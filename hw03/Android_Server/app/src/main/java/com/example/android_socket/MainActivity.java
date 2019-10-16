package com.example.android_socket;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    public EditText text, port;
    public TextView ip, chattings, chat, chat2;
    public DataInputStream dataInputStream;
    public DataOutputStream dataOutputStream;
    public String readtext, writetext, recv, send;

    @Override
    protected void onCreate(Bundle savedInstanceState) { // onCreate
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // findViewById 사용
        ip = (TextView) findViewById(R.id.ip);
        port = (EditText) findViewById(R.id.port);
        text = (EditText) findViewById(R.id.msg);
        chattings = (TextView) findViewById(R.id.chattings);

        try {
            ip.setText(getLocalIpAddress());
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
    }

    public void ServerOpen(View view) { // 서버 오픈
        new Thread() { // 쓰레드
            public void run() { // run
                try {
                    ServerSocket socket = new ServerSocket(); // 서버 소켓 생성
                    socket.bind(new InetSocketAddress(Integer.parseInt(port.getText().toString()))); // bind
                    Socket s = socket.accept(); // 소캣 s를 생성하여 서버소켓을 accept
                    dataInputStream = new DataInputStream(s.getInputStream()); // 데이터 입력
                    dataOutputStream = new DataOutputStream(s.getOutputStream()); // 데이터 출력
                    recvServer();
                } catch (Exception e) { // exception
                    e.printStackTrace();
                }
            }
        }.start(); // 쓰레드 실행
    }

    public void recvServer() { // 클라이언트로부터 text를 받음
        new Thread() { // 쓰레드
            public void run() { // run
                try {
                    while (true) {
                        readtext = dataInputStream.readUTF();
                        runOnUiThread(new Runnable() { // runOnUiThread
                            public void run() { // run
                                chat = (TextView) findViewById(R.id.chattings); // chat findViewById
                                recv = "[RECV]"; // 수신완료를 출력하기 위해 생성
                                readtext = recv.concat(readtext); // concat
                                chat.setText(readtext); // setText
                            }
                        });
                    }
                } catch (IOException e) { // exception
                    e.printStackTrace();
                }
            }
        }.start();
    }

    public void SendClient(View view) { // 클라이언트로 text를 보냄
        new Thread() { // 쓰레드
            public void run() { // run
                try {
                    writetext = text.getText().toString();
                    dataOutputStream.writeUTF(writetext);
                    runOnUiThread(new Runnable() { // runOnUiThread
                        public void run() { // run
                            chat2 = (TextView) findViewById(R.id.chattings); // chat2 findViewById
                            send = "[SEND]"; // 송신완료를 출력하기 위해 생성
                            writetext = send.concat(writetext); // concat메소드로
                            chat2.setText(writetext); // setText
                        }
                    });
                } catch (IOException e) { // exception
                    e.printStackTrace();
                }
            }
        }.start();
    }

    public String getLocalIpAddress() throws UnknownHostException { // 휴대폰 IP주소 앱에 출력
        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        assert wifiManager != null;
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int ipInt = wifiInfo.getIpAddress();
        return InetAddress.getByAddress(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(ipInt).array()).getHostAddress();
    }
}