function checkPassword(str) {
    let code, i, len;
    let numbers = false;
    let letters = false;
    let invalid = false;
    for (i = 0, len = str.length; i < len; i++) {
        code = str.charCodeAt(i);
        if(!(code >= 32 && code <= 126)){
            invalid = true;
        }
        if (code > 47 && code < 58) {
            numbers = true;
        }
        if((code > 64 && code < 91) || (code > 96 && code < 123)){
            letters = true;
        }
    }
    if(invalid){
        return 0;
    }
    else if(numbers && !letters){
        return 1;
    }
    else if(letters && !numbers){
        return 2;
    }
    else if(str.length < 9){
        return 3;
    }
    else{
        return -1;
    }
}