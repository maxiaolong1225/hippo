
export default {
  HOST:'http://api.hippo.com:8000',
  WS_HOST:'ws://api.hippo.com:8000',
  check_login(ths){
    let token = sessionStorage.token || localStorage.token
    if (!token){
      this.$router.push('/');

    };

    // 校验token有效性

    ths.$axios.post(`${ths.$settings.HOST}/users/verify/`,{
      token: token,
    }).then((res)=>{
      console.log(res);

      sessionStorage.token = res.data.token;

    }).catch((error)=>{
      this.$router.push('/');
    });
    return token
  }
}
