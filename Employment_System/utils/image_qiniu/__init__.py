from qiniu import Auth, put_file, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'v1R6oyd4ioeA9kroKQkmIHchKvXVlc397zsiZetl'
secret_key = 'XTEthTgDJkvEAQLMNNXagyXyKkKR0-Lo5hbohr_F'

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 要上传的空间
bucket_name = 'icong'
url_prefix = 'http://r7pjj3wfv.bkt.clouddn.com/'


def upload_image_to_qiniu(localfile, key):
    # 上传后保存的文件名
    # key = '天蝎.png'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = './兔子女孩.jpg'

    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    return url_prefix + key


if __name__ == '__main__':
    upload_image_to_qiniu()