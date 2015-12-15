using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using RuleRequest;
using System.ServiceModel;
using System.ServiceModel.Description;
using System.ServiceModel.Web;


namespace BaseMain
{
    class Program
    {
        static void Main(string[] args)
        {
            RestDemoServices DemoServices = new RestDemoServices();
            WebHttpBinding binding = new WebHttpBinding();
            WebHttpBehavior behavior = new WebHttpBehavior();
            

            Console.WriteLine("press any key to exit now");

            WebServiceHost _serviceHost = new WebServiceHost(DemoServices, new Uri("http://localhost:8000/DEMOService"));
           ;
            _serviceHost.AddServiceEndpoint(typeof(BaseEntry.IRESTDemoServices), binding, "");
            _serviceHost.Open();
            Console.ReadKey();
            _serviceHost.Close();
        }
    }
}
