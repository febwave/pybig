
function SecDailyApi(url   
    , handlerSet){
    this.SearchSumHandler = handlerSet["searchSumHandler"];
    this.SearchInfoHandler = handlerSet["searchInfoHandler"];
    this.GetDetailsSumHandler = handlerSet["getDetailsSumHandler"];
    this.GetDetailsHandler = handlerSet["getDetailsHandler"];
    this.GetRangeTimeHandler = handlerSet["getRangeTimeHandler"];
    this.Url = url;
    this.TrID = 0;

}


SecDailyApi.prototype.resp_Exception = function (userDefined, response) {
    if (this.ExceptionHandler != null) {
        this.ExceptionHandler(userDefined,response);
    }
    else {
        alert(response);
    }
}

SecDailyApi.prototype.getNextTrID = function () {
    this.TrID = this.TrID + 1;
    return this.TrID;
}


SecDailyApi.prototype.OnDataArrived = function (connection, status, userDefined, pfnHandler) {
    if (connection.readyState == 4) {
        if (connection.status != 200) {
            this.resp_Exception(userDefined, connection.responseText)
            return;
        }
        var objResp = JSON.parse(connection.responseText);
        pfnHandler.call(this, userDefined, objResp);
    }  
  
}

SecDailyApi.prototype.sendRequest = function ( method, params,userDefined, pfnHandler) {
    var trID = this.getNextTrID();
   
    var inst = this;

    params["cookie"] = trID;

    var requestText = JSON.stringify(params);
    console.log("request %s ",requestText)
    $.ajax({
        type: 'POST'
            , url: this.Url + method
        , data: requestText
        , contentType: "application/json; charset=UTF-8"
        , complete: function (connection, status) {
            inst.OnDataArrived(connection, status, userDefined, pfnHandler)
        }
    }
    );
    return trID;
}

SecDailyApi.prototype.resp_SearchInfo = function ( userDefined,  result) {
    this.SearchInfoHandler(result["items"])
}

SecDailyApi.prototype.SearchInfo = function( filterText,offset,count){
    var params = {
        "filter": filterText,
        "offset": offset,
        "count": count};

    var trID =this.sendRequest( "secbatch", params,null,  this.resp_SearchInfo)
    return trID;
}

SecDailyApi.prototype.resp_SearchCount = function ( userDefined,  result) {

    var gotCount = result["total"];
    this.SearchSumHandler(gotCount);
}

SecDailyApi.prototype.SearchCount = function ( filterText) {

    var params = {
        "filter": filterText        
    };

    var trID =this.sendRequest( "secSum", params,null,  this.resp_SearchCount)
    return trID;
}

SecDailyApi.prototype.GetRangeTime = function (secCode,beginTime,closeTime,interval) {
    var params = {
        "code": secCode,
        "beginTime": beginTime,
        "closeTime": closeTime,
        "interval":interval
    };

    var trID =this.sendRequest( "rangeTotal", params,null,  this.resp_GetRangeTime)
    return trID;
}

SecDailyApi.prototype.resp_GetRangeTime = function(userDefined,  result){
    this.GetRangeTimeHandler(result["items"])
}

