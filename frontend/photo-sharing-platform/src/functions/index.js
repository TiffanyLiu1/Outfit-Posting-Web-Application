const checkIsLogin = function(logedInAccount) {
    const curTime = new Date().getTime();
    // Have account information and have not expired
    if (logedInAccount && curTime < logedInAccount.expire) return true;
    else return false;
}

export {
    checkIsLogin
}