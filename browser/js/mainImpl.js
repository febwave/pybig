var mainImpl = mainImpl || {
        apiSession : null,
        dgObjects : null,
        filter:"",
        secOffset:0,
        secCount:10,
        secTotal:0
    };




mainImpl.OutputDebugString = function(text) {
    $("#debugOutput").attr("value", text);
};

mainImpl.ApiExceptionCallback = function(userDefined, response) {

}

mainImpl.FireSearchSumHandler = function(total) {
    if(total == 0 ){
        mainImpl.OutputDebugString("find no record")
    }
    if(mainImpl.secTotal == 0){
        mainImpl.secTotal = total;
        mainImpl.secOffset = 0;
        mainImpl.OnSearchFirst();
    }

mainImpl.ClearInfoDataGrid = function() {
        var tableName = "tbSecInfo";
        var columns = {
            "secCode": "code"
            , "secName": "name"
            , "secTime":"time"
            , "ns":"namespace"
            , "openPrice":"openPrice"
            , "closePrice":"closePrice"
            , "highPrice":"highPrice"
            , "lowPrice":"lowPrice"
            ,"exQty":"exQty"
            ,"changeTotal":"changeTotal"
        };
        if(mainImpl.dgObjects != null){
            mainImpl.dgObjects.ClearTable();
        }
        else {
            mainImpl.dgObjects = new dyncTable("resultListRegion", tableName, columns, false);
        }
    }

}

mainImpl.FireSearchInfoHandler = function(result) {
    mainImpl.ClearInfoDataGrid();

    for (var objItemIndex in result) {
        var objItem = result[objItemIndex]
        var fields = new Array();

        var columnIndex = 0;
        fields[columnIndex] = objItem[ "secCode"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "secName"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "secTime"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "ns"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "openPrice"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "closePrice"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "highPrice"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "lowPrice"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "exQty"];
        columnIndex = columnIndex+ 1;
        fields[columnIndex] = objItem[ "changeTotal"];
        columnIndex = columnIndex+ 1;

        mainImpl.dgObjects.AddRow( fields, false,mainImpl,true);
    }
    $("#resultListRegion").height($("#tbSecInfo").height());
}


mainImpl.doOnLoad = function(url)  {
    this.apiSession = new SecDailyApi(
        url
        , {
            searchSumHandler: mainImpl.FireSearchSumHandler,
            searchInfoHandler: mainImpl.FireSearchInfoHandler,
            getDetailsSumHandler: mainImpl.FireGetDetailsSumHandler,
            getDetailsHandler: mainImpl.FireGetDetailsHandler,
            getRangeTimeHandler: mainImpl.FireGetRangeTimeHandler
        }
    )
            
}

mainImpl.OnSearch =function(filterText) {
    var tableName = "tbFilter";

    mainImpl.OutputDebugString("")

    if(mainImpl.dgObjects != null) {
        mainImpl.dgObjects.DeleteTable()
    }
    var trID = mainImpl.apiSession.SearchCount(filterText,mainImpl.secOffset,mainImpl.secCount);
    mainImpl.filter = filterText;
}

mainImpl.OnSearchFirst = function(){
    mainImpl.secOffset = 0;
    mainImpl.apiSession.SearchInfo(mainImpl.filter,mainImpl.secOffset,mainImpl.secCount);

}

mainImpl.OnSearchPrev = function(){
    if(mainImpl.secOffset <  mainImpl.secCount){
        mainImpl.secOffset = 0
    }
    else{
        mainImpl.secOffset = mainImpl.secOffset -  mainImpl.secCount;
    }
    mainImpl.apiSession.SearchInfo(mainImpl.filter,mainImpl.secOffset,mainImpl.secCount);
}
mainImpl.OnSearchNext = function(){
    if(mainImpl.secOffset >= mainImpl.secTotal) {
        mainImpl.secOffset = mainImpl.secTotal - mainImpl.secCount;
    }
    else{
        mainImpl.secOffset = mainImpl.secOffset + mainImpl.secCount;
    }
    mainImpl.apiSession.SearchInfo(mainImpl.filter,mainImpl.secOffset,mainImpl.secCount);

}
mainImpl.OnSearchLast = function(){
    if(mainImpl.secTotal > mainImpl.secCount) {
        mainImpl.secOffset = mainImpl.secTotal - mainImpl.secCount;
    }
    else{
        mainImpl.secOffset = 0;
    }
    mainImpl.apiSession.SearchInfo(mainImpl.filter,mainImpl.secOffset,mainImpl.secCount);
    mainImpl.secOffset =  mainImpl.secTotal;
}

mainImpl.OnChangeBackColor=function(control, toChange) {
    var element = control;
    if (element) {
        if (toChange) {
            element.style.backgroundColor = "#C0C0C0";
        }
        else {
            element.style.backgroundColor = "#FFFFFF";
        }
    }
}

mainImpl.FireGetRangeTimeHandler = function(result){
    var ctx = document.getElementById("myChart").getContext("2d");


    var xItemArray = new Array();
    var yItemArray = new Array();
    var itemIndex = 0;
    for (var objItemIndex in result) {
        var objValue = result[objItemIndex];
        var baseTime = objValue["rangeTime"].substring(10);
        var count = objValue["count"];
        xItemArray[itemIndex] = baseTime;
        yItemArray[itemIndex] = count;
        itemIndex = itemIndex +1;
    }

    var data = {
        labels : xItemArray,
        datasets : [
            {
                fillColor : "rgba(220,220,220,0.5)",
                strokeColor : "rgba(220,220,220,1)",
                data : yItemArray
            }
        ]
    }

    new Chart(ctx).Line(data,null);

}

mainImpl.OnRowSelected = function(control,id) {
    var orgTime= control.children[2].innerHTML;
    var beginDate = orgTime.substring(0,10);
    var beginTime = beginDate + " 09:00:00";
    var closeTime = beginDate + " 17:00:00";

    var interval = parseInt( $("#interval").val());

    mainImpl.apiSession.GetRangeTime(id,beginTime,closeTime,interval);


}