import redis
import requests


class WeChatEnterprise:
    __DateBaseName = "WeChat"


    def __init__(self, corp_id: str, corp_secret: str, agent_id: str, redis_host: str, redis_port: int = 6379):
        self.r = redis.Redis(host=redis_host, port=redis_port)
        self.access_token = self.__get_access_token(corp_id, corp_secret)
        self.agent_id = agent_id


    def __get_access_token(self, corp_id: str, corp_secret: str) -> str:
        access_token = self.r.get(self.__DateBaseName + '_access_token')

        if access_token is None:
            response_dict = requests.get(url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
                                         params={"corpid": corp_id, "corpsecret": corp_secret}).json()
            if response_dict.get('errcode') != 0:
                raise Exception(
                    "error code: %d\nerror message: %s" % (response_dict.get('errcode'), response_dict.get("errmsg")))
            access_token = response_dict.get('access_token')
            self.r.setex(name=self.__DateBaseName + '_access_token', time=response_dict.get('expires_in'),
                         value=access_token)

        else:
            access_token = access_token.decode()

        return access_token


    def upload_media(self, filename: str, media_type: str = "file") -> str:
        media_id = self.r.get(self.__DateBaseName + '_file_' + filename)

        if media_id is None:
            files = {
                "media": (filename, open(filename, 'rb'), "multipart/form-data"),
            }
            response_dict = requests.post(
                url="https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (
                    self.access_token, media_type), files=files).json()
            if response_dict.get('errcode') != 0:
                raise Exception(
                    "error code: %d\nerror message: %s" % (response_dict.get('errcode'), response_dict.get("errmsg")))
            media_id = response_dict.get("media_id")
            self.r.setex(name=self.__DateBaseName + '_file_' + filename, time=3 * 24 * 60 * 60, value=media_id)

        else:
            media_id = media_id.decode()

        return media_id


    def upload_image(self):
        pass


    def send_text_message(self, content: str, to_user: str = "@all", safe: int = 0, enable_duplicate_check: int = 0,
                          duplicate_check_interval: int = 1800, msg_type: str = "text") -> requests.Response:
        data = {
            "touser": to_user,
            "msgtype": msg_type,
            "agentid": self.agent_id,
            "%s" % msg_type: {
                "content": content
            },
            "safe": safe,
            "enable_duplicate_check": enable_duplicate_check,
            "duplicate_check_interval": duplicate_check_interval
        }
        response = requests.post(
            url=" https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % self.access_token, json=data)
        return response


    def send_file_message(self, media_id: str, to_user: str = "@all", safe: int = 0, enable_duplicate_check: int = 0,
                          duplicate_check_interval: int = 1800) -> requests.Response:
        data = {
            "touser": to_user,
            "msgtype": "file",
            "agentid": self.agent_id,
            "file": {
                "media_id": media_id
            },
            "safe": safe,
            "enable_duplicate_check": enable_duplicate_check,
            "duplicate_check_interval": duplicate_check_interval
        }
        response = requests.post(
            url=" https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % self.access_token, json=data)
        return response
