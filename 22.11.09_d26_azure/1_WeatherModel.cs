// 온도, 습도, 미세먼지 data를 가져옴

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IoTClient
{
    internal class WeatherModel
    {
        public string DeviceID { get; set; }
        public int Temperature { get; set; }
        public int Humidity { get; set; }
        public int Dust { get; set; }
    }
}
