



function dyncTable(parent, tableName, columns, getDetail) {
    this.TableName = tableName;
    this.RowCount = 0
    var el_table = document.createElement("table")
    el_table.id = this.TableName;
    el_table.className = "lists"
    var el_body = document.createElement("tbody")
    el_body.id = this.TableName+"main"
    el_table.appendChild(el_body);

    this.MainControl = el_body;
    this.ParentControlName = parent;

    var el_Tr = document.createElement("tr");
    for (var columnKey in columns) {
        var el_Td = document.createElement("td");
        el_Td.id = "col_" + columns[columnKey];
        el_Td.width = 300;
        el_Td.className = "lyTableColumn";
        el_Td.innerHTML = columns[columnKey];
        el_Tr.appendChild(el_Td);
    }
    if (getDetail == true) {
        var el_Td = document.createElement("td");
        el_Td.id = "col_DETAILS" ;
        el_Td.width = 300;
        el_Td.innerHTML = "details";
        el_Td.className = "lyTableColumn"
        el_Tr.appendChild(el_Td);
    }
    el_body.appendChild(el_Tr);


    document.getElementById(parent).appendChild(el_table)

}



dyncTable.prototype.AddRow = function ( fields, getDetail,parent,enabledRowSelected) {

    var tr=document.createElement("tr" );
    tr.className =  "tr_" + this.TableName;

    tr.onmouseover = function(){
        parent.OnChangeBackColor(this,true);
    }

    tr.onmouseout =function(){
        parent.OnChangeBackColor(this,false);
    }
    if(enabledRowSelected == true) {
        tr.ondblclick = function () {
            parent.OnRowSelected(this, fields[0]);
        }
    }

    tr.id="row_"+fields[0];
    for(var fIndex=0;fIndex<fields.length;fIndex++)
    {
        var td=document.createElement("td");
        td.id = tr.id + "fd_"+fIndex;

        td.className = "clsTD_" + this.TableName + "_"+fIndex;
        td.appendChild(document.createTextNode(fields[fIndex]));
        tr.appendChild(td);
    }
    if (getDetail == true) {
        var td = document.createElement("td");
        td.id = tr.id + "fd_details";
        var btnDetail = document.createElement("input");
        btnDetail.type = "button";
        btnDetail.id = "btnDetail";
        btnDetail.value = "Details";

        btnDetail.onclick = function(){
            dyncTable.getParent(parent).OnGetDetails(fields[0]);
        }

        td.appendChild(btnDetail);
        tr.appendChild(td);
    }
    this.MainControl.appendChild (tr);
    this.ClearFocus();
}

dyncTable.prototype.RemoveRow = function (controlName, id) {
    var bodyName = dyncTable.getMainBody(controlName);
    var body = document.getElementById(bodyName)

    var element = $("#row_"+id);
    if(element)
        element.remove();
    dyncTable.ClearFocus(body);
}

dyncTable.prototype.DeleteTable = function () {

    var body = this.MainControl;
    if (body != null) {
        var currentControl;
        currentControl = document.getElementById(this.TableName)
        document.getElementById(this.ParentControlName).removeChild(currentControl);
    }
}

dyncTable.prototype.ClearTable = function() {

    var body = this.MainControl

    if(	 body.children.length == 1)
    {
        return;
    }

    for(var lastIndex = body.children.length-1; lastIndex > 0;lastIndex--)
    {
        var element = body.children[lastIndex];
        body.removeChild(element);
    }

}

dyncTable.prototype.ClearFocus = function(controlName) {
    var body = this.MainControl

    for(var lastIndex = body.children.length-1; lastIndex > 0;lastIndex--)
    {
        var element = body.children[lastIndex];
        element.style.backgroundColor="#FFFFFF";
    }
}

dyncTable.prototype.UpdateRow = function(controlName,id,newValue) {
    var bodyName = dyncTable.getMainBody(controlName);
    var body = document.getElementById(bodyName)

    var fdControl = document.getElementById("row_"+id + "fd_1");
    fdControl.innerHTML = newValue;
    dyncTable.ClearFocus(body);
}

dyncTable.prototype.FocusRow = function(id){
    var element = document.getElementById("row_"+id);
    if(element)
    {
        element.style.backgroundColor="#664455";
    }
}
