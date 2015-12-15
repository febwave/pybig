using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Runtime.Serialization;

namespace BaseEntry
{
    
    public class SecSumRequest
    {
       
        public string  filter { get; set; }
       
        public int cookie { get; set; }
    }


    
    public class SecSumResponse
    {
        public int total { get; set; }
        public int cookie { get; set; }
    }       
    

    public class SecBatchRequst
    {
        public string filter { get; set; }
        public int offset { get; set; }
        public int count { get; set; }
        public int cookie { get; set; }
    }

    public class SecInfo
    {
        public string secCode { get; set; }
        public string secName { get; set; }
        public string ns { get; set; }
        public string secTime { get; set; }
        public double openPrice { get; set; }
        public double closePrice { get; set; }
        public double highPrice { get; set; }
        public double lowPrice { get; set; }
        public int changeTotal { get; set; }
        public double exQty { get; set; }        
    }

    public class SecResponse
    {
        public int cookie { get; set; }
        public List<SecInfo> items { get; set; }
    }


    public class SecDetailSumRequest
    {
        public int cookie { get; set; }
        public string code { get; set; }
    }

    public class SecDetailSumResponse
    {
        public int cookie { get; set; }
        public int total { get; set; }
    }  


    public class SecDetailBatchRequst
    {        
        public string code { get; set; }
        public int offset { get; set; }
        public int count { get; set; }
        public int cookie { get; set; }
    }


    public class SecDetail
    {
        public int seq {get;set;}
        public string detailTime { get; set; }
    }

    public class SecDetailBatchResponse
    {       
        public int cookie { get; set; }
        public List<SecDetail> items { get; set; }
    }

    public class SecRangeRequest
    {
        public int cookie { get; set; }
        public string code { get; set; }
        public int interval { get; set; }
        public string beginTime { get; set; }
        public string closeTime { get; set; }
    }

    public class SecRangeItem
    {
        
        public string rangeTime { get; set; }
        public int count { get; set; }
    }

    public class SecRangeResponse
    {
        public int cookie { get; set; }
        public List<SecRangeItem> items { get; set; }
    }


    [ServiceContract(Name = "RESTDemoServices")]
    public interface IRESTDemoServices
    {
        [OperationContract]
        [WebInvoke(UriTemplate = "secSum", Method = "*", BodyStyle = WebMessageBodyStyle.Bare, RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        SecSumResponse GetSecSum(SecSumRequest req);

        [OperationContract]
        [WebInvoke(UriTemplate = "secbatch", Method = "*", BodyStyle = WebMessageBodyStyle.Bare, RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        SecResponse GetSecList(SecBatchRequst req);


        [OperationContract]
        [WebInvoke(UriTemplate = "detailSum", Method = "*", BodyStyle = WebMessageBodyStyle.Bare, RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        SecDetailSumResponse GetDetailSum(SecDetailSumRequest req);

        [OperationContract]
        [WebInvoke(UriTemplate = "detailbatch", Method = "*", BodyStyle = WebMessageBodyStyle.Bare, RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        SecDetailBatchResponse GetDetailList(SecDetailBatchRequst req);

        [OperationContract]
        [WebInvoke(UriTemplate = "rangeTotal", Method = "*", BodyStyle = WebMessageBodyStyle.Bare, RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        SecRangeResponse GetRangeTotal(SecRangeRequest req);
    }
}

