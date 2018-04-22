using System;
using StockSharp.Messages;
using StockSharp.Quik;

using System.Runtime.InteropServices;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace ConsoleApplication1
{
    class Program
    {
        [DllImport(@"PushTrade.dll", EntryPoint = "Add", CallingConvention = CallingConvention.StdCall)]
        public static extern double Add(string dir, string name, float price, float quantity, string time, string sign);
  
        [DllImport("kernel32.dll")]
        static extern IntPtr GetConsoleWindow();

        [DllImport("user32.dll")]
        static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        const int SW_HIDE = 0;
        const int SW_SHOW = 5;
       
        static public void Main()
        {
            
            var handle = GetConsoleWindow();


            ShowWindow(handle, SW_HIDE);
   

            QuikTrader _trader = null;

            if (_trader == null || _trader.ConnectionState == ConnectionStates.Disconnected)
            {
                if (_trader == null)
                {

                    //for(int i = 2; i < 20; i++) {
                    //    var direct = "";
                    //    var prc = 1;
                    //        if (i % 2 == 0)
                    //    {
                    //        direct = "buy";
                    //        prc = 100;
                    //    }
                    //    else
                    //    {

                    //        direct = "sel";
                    //        prc = 110;
                    //    }
                    //    Tuple<string, string, float, float,string, string> sdelka = new Tuple<string, string, float, float, string, string>(direct, "SBER", prc, 2, "SBER", "");
                    //    //var sec_code = sdelka.Item2;

                    //    //var position_direction = sdelka.Item1;
                    //    //var price = sdelka.Item3;

                    //    //var quantity = sdelka.Item4;
                    //    //var time = sdelka.Item5;
                    //    //var sign = "";
                    //    //Add(position_direction, sec_code, price, quantity, time, sign);
                    //    System.Threading.Thread.Sleep(5000);
                    //}
                    
                    var cicle = 1;
                    
                    //TODO сделать проверку на конкретный терминал
                    var terminal = QuikTerminal.GetDefaultPath();


                    _trader = new QuikTrader(terminal) { IsDde = false };
                    _trader.ReConnectionSettings.AttemptCount = 10;
                    _trader.ReConnectionSettings.Interval = TimeSpan.FromSeconds(5);
                 

                    _trader.Connected += () =>
                    {
                        while (cicle == 1)
                        {
                            _trader.NewMyTrade += trade =>
                            {
                            var commision = trade.Commission.Value;
                            var position_direction = trade.Trade.OrderDirection.Value.ToString();
                            var price = (float)trade.Trade.Price;
                            var sec_code = trade.Trade.Security.Code.ToString();
                            var quantity =(float) trade.Trade.Volume;
                            var time = trade.Trade.Time.ToUniversalTime().ToString();
                            var sign = "";
                                Add(position_direction,sec_code,price,quantity,time,sign);
                           
    };
                        }

                    };
                   
                    while( _trader.ConnectionState == ConnectionStates.Disconnected){
  _trader.Connect();
                    }
 
                }
            }
        }


   
            }
        }
    
