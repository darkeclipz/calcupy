class HTTP {
    post(endpoint, object, successCallback, errorCallback) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", endpoint, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() { 
            if(this.status == 200) successCallback(JSON.parse(this.responseText)); 
            else                   errorCallback(this.responseText)
        }
        xhr.send(JSON.stringify(object));
    } 
}