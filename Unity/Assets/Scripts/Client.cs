// ZeroMQ library for C#
using NetMQ;
using NetMQ.Sockets;
// System libraries
using System;
using System.Threading;
using System.Collections.Generic;
// Default Json library for work with json
using Newtonsoft.Json;
// Unity Engine
using UnityEngine;

// Set up dictonary for receive data
public class Dict
{
    [JsonProperty("dtype")]
    public string dtype { get; set; }

    [JsonProperty("shape")]
    public List<int> shape { get; set; }

    [JsonProperty("data")]
    public List<List<float>> data { get; set; }
}

public class Client : MonoBehaviour
{
    // prepare client Thread
    private Thread tcpListenerThread;
    // get joints root
    public Joint m_root;
    // bool if is data
    private static bool move = false;
    // dict class
    public static Dict dict;
    // check collision bool
    public static bool is_collision = false;
    // iteration variable
    public static int i;

    // automatically update and if not collision and data do motion
    private void FixedUpdate()
    {
        if (!is_collision && move)
        {
            try
            {
                // from root joint move
                Joint current = m_root;

                // load data from dict
                current.transform.localEulerAngles = new Vector3(0, 0, (-1) * (float)dict.data[i][0]);
                current = current.GetChild();

                current.transform.localEulerAngles = new Vector3(90, 0, (-1) * (float)dict.data[i][1]);
                current = current.GetChild();

                current.transform.localEulerAngles = new Vector3(0, 0, (-1) * (float)dict.data[i][2]);
                current = current.GetChild();

                current.transform.localEulerAngles = new Vector3(0, 0, (-1) * (float)dict.data[i][3]);
                current = current.GetChild();

                current.transform.localEulerAngles = new Vector3(90, 0, (-1) * (float)dict.data[i][4]);
                current = current.GetChild();

                current.transform.localEulerAngles = new Vector3(270, 0, (-1) * (float)dict.data[i][5]);
            }

            catch (Exception e)
            {
                Debug.Log("Exception:" + e);
            }
        }
    }
    void Start(){
        // Start TcpServer background thread 		
        tcpListenerThread = new Thread(new ThreadStart(ListenForIncommingRequests));
        tcpListenerThread.IsBackground = true;
        tcpListenerThread.Start();
        Debug.Log("Start Thread");
    }

    private void ListenForIncommingRequests(){
        try
        {
            using (var client = new RequestSocket())
            {
                // connect to server
                client.Connect("tcp://127.0.0.1:5555");
                // send message
                client.SendFrame("Start Compute");
                // receive dictonary
                var msg = client.ReceiveFrameString();
                // convert to dict
                dict = JsonConvert.DeserializeObject<Dict>(msg);
                // data is in class
                move = true;
                // iterate throu main and low Thread
                for (int k = 0; k < dict.shape[0]; k++)
                {
                    i += 1;
                    Thread.Sleep(10);
                }
            }

            move = false;

        }
        catch (Exception socketException)
        {
            Debug.Log("SocketException " + socketException);
        }
    }

    // On quit application -> end tasks
    void OnApplicationQuit()
    {
        Thread.Sleep(10);
        Debug.Log("End Thread");
        // !!!! - Neccesary for quit NetMQ libary -> multiple run issue!
        NetMQConfig.Cleanup();
    }
}