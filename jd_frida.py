import frida
import json

rpc_sign = """
rpc.exports = {
    getsign: function(function_id, body_string, uuid){
      var sig = "";
      Java.perform(
        function(){
            //拿到context上下文
            var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
            var context = currentApplication.getApplicationContext();
            var BitmapkitUtils = Java.use('com.jingdong.common.utils.BitmapkitUtils');
            sig = BitmapkitUtils.getSignFromJni(context, function_id, body_string, uuid, 'android', '9.2.0');
            
            
            //console.log(context, uuid)
        } 
      )
       return sig;
    }
};

"""


def get_sign(function_id, body_string, u):
    process = frida.get_remote_device().attach('com.jingdong.app.mall')
    script = process.create_script(rpc_sign)
    script.load()
    sign = script.exports.getsign(function_id, body_string, u)
    return sign


if __name__ == '__main__':
    body_data = {"appId": "jd.mall",
                 "content": "tbV8seY199tCdw6GllmkWyCNNENuGsgwLByA7svt5HbPXvlI9wQhHMk3dT7f0ldfpq6M0MCiUD+A\nVrY390Yct0FSub03INUml9n1bS9rZSF3XT0q1kQdehKPO4CccMiEA6NQXYiqYn9wLsDDYEIjmkVA\nEbXI88CwO0K7uhwemdhQMZrcIFj6jMmyiDNDxSA1OjFw88hR0oSCF0m8ll9o9iU2MVSHDipF5ZDn\nFR4E+82mwfRYIxamafB+nWG8GuHcKhiQOWGbChTcG3TxcGT053wfcc6uuMD7+L4PcsNRQjM9syFc\nXR6FBu/sCV/kH/3rT8w/m3zV1c9JpW9lq/7WVzCVvAIj7RNt2zzYFisymCE="}
    body_string = json.dumps(body_data, ensure_ascii=False).replace(" ", "")
    function_id = 'liveauth'
    u = '-a08d16f38776'
    sign = get_sign(function_id, body_string, u)
    print(sign)
