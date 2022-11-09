
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
        private const string DeviceConnectionString = "XXXXX"; // IoT Hub > 공유 액세스 정책 > iot hub owner > 기본연결 문자열
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

        private static void SetTimer() // Timer: 2초에 한번씩 호출 
        {
            SensorTimer = new System.Timers.Timer(2000);  // 2초
            SensorTimer.Elapsed += SensorTimer_Elapsed;  // Event 
            SensorTimer.AutoReset = true;
            SensorTimer.Enabled = true;
        }

        private static async void SensorTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            Console.WriteLine("The Elapshed event was raised at {0:HH:mm:ss.fff}", e.SignalTime );

            // Process 보다 작은 단위 Thread (Process > Thread)
            await SendEvent();  // Device에서 Cloud로 message send, await: 비동기 호출
            await ReceiveCommands();  // Cloud에서 Device로 message 보냈는지 확인
        }

        
        private static async Task SendEvent() // Device에서 Cloud로 message send
                                                // async : 비동기적 > 별도의 thread 필요 > 실행 이후
                                                // 항상 sync Task로 해야함 (Task을 return 함)
        {
            WeatherModel model = DummySensor.GetWeatherModel(DeviceID);  // dummy값 가져오기 

            
            string json = Newtonsoft.Json.JsonConvert.SerializeObject(model);  // json 형태로 변환

            Console.WriteLine(json);  // json 파일 content 출력

            Message message = new Message(Encoding.UTF8.GetBytes(json));  // Encoding
            await SensorDevice.SendEventAsync(message);  // 비동기 호출시 await 필요 !!!
                                                         // Device를 추상화 한 객체 (SensorDevice에게 전송 >> IoT Hub로 쏴줘 !! )
        }

        private static async Task ReceiveCommands()  // Cloud에서 Device로 message send
        {
            Message receivedMessage;
            string messageData;

            receivedMessage = await SensorDevice.ReceiveAsync(TimeSpan.FromSeconds(1));  // receive message

            if (receivedMessage != null)  // message 내용이 null이 아니라면
            {
                messageData = Encoding.ASCII.GetString(receivedMessage.GetBytes());  // Encoding
                Console.WriteLine("\t{0}> Received message: {1}", DateTime.Now.ToLocalTime(), messageData);

                await SensorDevice.CompleteAsync(receivedMessage);
            }
        }


    }
}
