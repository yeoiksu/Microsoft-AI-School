
// Sensor Program (Weather Model)
//

using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Mail;
using System.Text;
using System.Threading.Tasks;

using System.Timers;
using Microsoft.Azure.Devices.Client;  // IoT Hub와 연결하기 위한 Pacakage
using Newtonsoft;  // json 관련 pacakage

namespace IoTClient
{
    internal class Program
    {
        private static System.Timers.Timer SensorTimer;
        private const string DeviceConnectionString = "XXXXXXXXXXXXXX"; // IoT Hub > 공유 액세스 정책 > iot hub owner > 기본연결 문자열
        private const string DeviceID = "device1";  // IoT Hub 에서 직접 생성했던 device 이름 
        private static DeviceClient SensorDevice = null;  // IoT Hub와 연결할 객체

        private static DummySensor DummySensor = new DummySensor();  
        static void Main(string[] args)
        {
            SetTimer();

            SensorDevice = DeviceClient.CreateFromConnectionString(DeviceConnectionString, DeviceID);  // 접속
            
            if(SensorDevice == null)  // 연결 실패했을 경우
            {
                Console.WriteLine("Failed to create DeviceClient !!");
                SensorTimer.Stop();  // Timer Stop 
            }

            Console.WriteLine("\nPress Enter Key to exit the application...\n");
            Console.WriteLine("The application started at {0:HH:mm:ss.fff}", DateTime.Now );
            Console.ReadLine();
            SensorTimer.Stop();
            SensorTimer.Dispose();
        }

        private static void SetTimer() // 2초 Timer
        {
            SensorTimer = new System.Timers.Timer(2000);  // 2초
            SensorTimer.Elapsed += SensorTimer_Elapsed;  // Event 
            SensorTimer.AutoReset = true;
            SensorTimer.Enabled = true;
        }

        private static void SensorTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            Console.WriteLine("The Elapshed event was raised at {0:HH:mm:ss.fff}", e.SignalTime );
            SendEvent();  // SendEvent() 실행
        }

        private static void SendEvent()
        {
            WeatherModel model = DummySensor.GetWeatherModel(DeviceID);  // dummy값 가져오기 

            string json = Newtonsoft.Json.JsonConvert.SerializeObject(model);  // json 형태로 변환

            Console.WriteLine(json);  // json 파일 content 출력

        }

    }
}
