using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.ServiceModel;
using System.ServiceModel.Web;
using BaseEntry;
using System.ServiceModel.Activation;
using MySql.Data.MySqlClient;

namespace RuleRequest
{
    [ServiceBehavior(InstanceContextMode = InstanceContextMode.Single, ConcurrencyMode = ConcurrencyMode.Single, IncludeExceptionDetailInFaults = true)]
    [AspNetCompatibilityRequirements(RequirementsMode = AspNetCompatibilityRequirementsMode.Allowed)]
    [JavascriptCallbackBehavior(UrlParameterName = "callback")]
    public class RestDemoServices : BaseEntry.IRESTDemoServices
    {
        private MySqlConnection openDataBase(string cmdSql, out MySqlDataReader reader)
        {
            string serverAddress = "192.168.237.144";
            string userName = "root";
            string userPassword = "bnm123";
            string connStr = String.Format("server={0};user id={1}; password={2}; database=mystore; pooling=false", serverAddress, userName, userPassword);
            MySqlConnection conn = new MySqlConnection(connStr);
            conn.Open();

            MySqlCommand cmd = new MySqlCommand(cmdSql, conn);
            reader = cmd.ExecuteReader();
            return conn;
        }

        private void closeDataBase(MySqlConnection conn)
        {
            conn.Close();
        }   

        public SecSumResponse GetSecSum(SecSumRequest req)
        {
            
            if (WebOperationContext.Current.IncomingRequest.Method == "OPTIONS")
            {
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Methods", "POST");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Accept");

                return null;
            }
            WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
            SecSumResponse resp = new SecSumResponse();
            resp.cookie = req.cookie;            
            MySqlConnection conn = null;
            MySqlDataReader reader = null;
            string cmdSql = null;
            try
            {
                if (req.filter == null || req.filter.Trim().Length == 0)
                {
                    cmdSql = string.Format("select count(tID) from secDaily;");
                }
                else
                {
                    cmdSql = string.Format("select count(tID) from secDaily where secCode like '%{0}%' or secName like '%{0}%';", req.filter.Trim());
                }
                conn = openDataBase(cmdSql,out reader);
                while (reader.Read())
                {
                    resp.total = reader.GetInt32(0);
                }                
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("GetSecSum: " + ex.Message);
            }
            finally
            {
                if (reader != null)
                {
                    reader.Close();
                }
                if (conn != null)
                {
                    closeDataBase(conn);
                }
            }
            return resp;
        }

        public  SecResponse GetSecList(SecBatchRequst req)
        {
            if (WebOperationContext.Current.IncomingRequest.Method == "OPTIONS")
            {
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Methods", "POST");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Accept");

                return null;
            }
            WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
            SecResponse resp = new SecResponse();
            MySqlConnection conn = null;
            MySqlDataReader reader = null;
            string cmdSql = null;

           

            try
            {
                resp.cookie = req.cookie;
                resp.items = new List<SecInfo>();
                if (req.filter == null || req.filter.Trim().Length == 0)
                {
                    cmdSql = string.Format("select secCode,secName,ns,DATE_FORMAT(secTime,'%Y-%m-%d %H:%i:%S'),openPrice,closePrice,highPrice,lowPrice,changeTotal,exQty " +
                                          "from secDaily order by  secCode limit {0},{1};"
                                          , req.offset, req.count);
                }
                else
                {
                    cmdSql = string.Format("select secCode,secName,ns,DATE_FORMAT(secTime,'%Y-%m-%d %H:%i:%S'),openPrice,closePrice,highPrice,lowPrice,changeTotal,exQty " +
                                            "from secDaily where secCode like '%{0}%' or secName like '%{0}%'  order by  secCode limit {1},{2};"
                                            , req.filter.Trim(),req.offset,req.count);
                }
                conn = openDataBase(cmdSql, out reader);
                while (reader.Read())
                {
                    SecInfo detail = new SecInfo();
                    detail.secCode = reader.GetString(0);
                    detail.secName = reader.GetString(1);
                    detail.ns = reader.GetString(2);
                    detail.secTime = reader.GetString(3).ToString();
                    detail.openPrice = reader.GetDouble(4);
                    detail.closePrice = reader.GetDouble(5);
                    detail.highPrice = reader.GetDouble(6);
                    detail.lowPrice = reader.GetDouble(7);
                    detail.changeTotal = reader.GetInt32(8);
                    detail.exQty = reader.GetDouble(9);


                    resp.items.Add(detail);
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("GetSecSum: " + ex.Message);
            }
            finally
            {
                if (reader != null)
                {
                    reader.Close();
                }
                if (conn != null)
                {
                    closeDataBase(conn);
                }
            }
            return resp;
        }

        public SecDetailSumResponse GetDetailSum(SecDetailSumRequest req)
        {

            if (WebOperationContext.Current.IncomingRequest.Method == "OPTIONS")
            {
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Methods", "POST");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Accept");

                return null;
            }
            WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
            SecDetailSumResponse resp = new SecDetailSumResponse();
            resp.cookie = req.cookie;        
            MySqlConnection conn = null;
            MySqlDataReader reader = null;
            string cmdSql = null;

            
            try
            {

                if (req.code == null || req.code.Trim().Length == 0)
                {
                    return resp;
                }
                
                
                cmdSql = string.Format("  select count(sdID) from secDetail  " +
                      "inner join secDaily on secDetail.secDailyID = secDaily.tID "+
                      "where secDaily.secCode = '{0}';"
                      , req.code.Trim());
                
                conn = openDataBase(cmdSql, out reader);
                while (reader.Read())
                {
                    resp.total = reader.GetInt32(0);
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("GetSecSum: " + ex.Message);
            }
            finally
            {
                if (reader != null)
                {
                    reader.Close();
                }
                if (conn != null)
                {
                    closeDataBase(conn);
                }
            }
            return resp;
        }

        public SecDetailBatchResponse GetDetailList(SecDetailBatchRequst req)
        {
            if (WebOperationContext.Current.IncomingRequest.Method == "OPTIONS")
            {
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Methods", "POST");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Accept");

                return null;
            }
            WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
            SecDetailBatchResponse resp = new SecDetailBatchResponse();
            MySqlConnection conn = null;
            MySqlDataReader reader = null;
            string cmdSql = null;
            resp.cookie = req.cookie;        
            try
            {
                            
                if (req.code == null || req.code.Trim().Length == 0)
                {
                    return resp;
                }
                resp.items = new List<SecDetail>();


                cmdSql = string.Format("select seq,DATE_FORMAT(detailTime,'%Y-%m-%d %H:%i:%S') from secDetail  " +
                      "inner join secDaily on secDetail.secDailyID = secDaily.tID " +
                      "where secDaily.secCode = '{0}'  order by seq  limit {1},{2}; "
                                            , req.code.Trim(), req.offset, req.count);
                
                conn = openDataBase(cmdSql, out reader);
                while (reader.Read())
                {
                    SecDetail detail = new SecDetail();
                    detail.seq = reader.GetInt32(0);
                    detail.detailTime = reader.GetString(1);
                    
                    resp.items.Add(detail);
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("GetDetailList: " + ex.Message);
            }
            finally
            {
                if (reader != null)
                {
                    reader.Close();
                }
                if (conn != null)
                {
                    closeDataBase(conn);
                }
            }
            return resp;
        }

        public SecRangeResponse GetRangeTotal(SecRangeRequest req)
        {
            if (WebOperationContext.Current.IncomingRequest.Method == "OPTIONS")
            {
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Methods", "POST");
                WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Headers", "Content-Type, Accept");

                return null;
            }
            WebOperationContext.Current.OutgoingResponse.Headers.Add("Access-Control-Allow-Origin", "*");
             
            SecRangeResponse resp = new SecRangeResponse();
            MySqlConnection conn = null;
            MySqlDataReader reader = null;
            string cmdSql = null;
            resp.cookie = req.cookie;        
            try
            {
                string codeRange;     
                if (req.code == null || req.code.Trim().Length == 0)
                {
                    codeRange = "";
                }
                else
                {
                    codeRange = req.code.Trim();
                }
                resp.items = new List<SecRangeItem>();


                cmdSql = string.Format("call getrange('{0}','{1}','{2}',{3});", codeRange,req.beginTime,req.closeTime,req.interval );
                
                conn = openDataBase(cmdSql, out reader);
                while (reader.Read())
                {
                    SecRangeItem detail = new SecRangeItem();
                    detail.rangeTime = reader.GetString(0);
                    detail.count = reader.GetInt32(1);
                  
                    
                    resp.items.Add(detail);
                }
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("GetRangeTotal: " + ex.Message);
            }
            finally
            {
                if (reader != null)
                {
                    reader.Close();
                }
                if (conn != null)
                {
                    closeDataBase(conn);
                }
            }
            return resp;
        }

     
    }
}
