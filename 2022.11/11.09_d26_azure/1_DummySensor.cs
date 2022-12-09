using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IoTClient
{
    internal class DummySensor
    {
        // random dummy값을 부여하여 model을 리턴함
        private Random _Random = new Random();

        public WeatherModel GetWeatherModel(string deviceID)
        {
            var model = new WeatherModel();
            model.DeviceID = deviceID;
            model.Temperature = _Random.Next(20, 35);  // random temperature값
            model.Humidity = _Random.Next(40, 80);  // random Humidity값 
            model.Dust = model.Temperature + 50 + _Random.Next(1,5);  // random dust값

            return model;
        }
    }
}
