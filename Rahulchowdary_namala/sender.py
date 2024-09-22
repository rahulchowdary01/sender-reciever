from socket import *
from util import *
from time import sleep
server_name="0.0.0.0"
server_port=10516
client_socket=socket(AF_INET,SOCK_DGRAM)
class Sender:
  #initializing the data and socket
  def __init__(self):
      self.count=1
      #initialized sequence and acknowledgement to 0
      self.seq=0
      self.ack=0
      #creating a socket
      self.client_socket = socket(AF_INET, SOCK_DGRAM)
      """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
  def rdt_send(self, app_msg_str):
        print("original string:",app_msg_str)
        timeout_duration = 3  # Timeout duration in seconds
        #if the sequence number is zero
        if(self.seq==0):
          #if the acknowledgement number is zero
          if(self.ack==0):
            app_msg_bytes = app_msg_str.encode('utf-8')
            #creating a packet
            l = make_packet(app_msg_bytes, self.ack, self.seq)
            print("packet created:",l)
            #sending data to the reciever
            self.client_socket.sendto(l, (server_name, server_port))
            print("packet num.",self.count,"is successfully sent to the reciever.")
            #if data recieved and count is 3
            if(self.count%3==0):
              #the values can divided with both 3 and 6
              if(self.count%6==0):
                #if value divided by 6 perform timeout
                print("socket timeout! resend!\n")
                print("[timeout retransmission]:",app_msg_str)
                self.count+=1
                print("packet num.",self.count,"is successfully sent to the reciever.")
                p=self.rdt_retransmit(app_msg_str,0,0)   
                self.ack=p
                #   self.seq+=1 
              else:
                #if the value divided by 3 perform retransmission
                print("reciever ACK previous packet,resend!\n")
                print("[ACK -previous retransmission]:",app_msg_str)
                self.count+=1
                print("packet num.",self.count,"is successfully sent to the reciever.")
                p=self.rdt_retransmit(app_msg_str,0,0)
                self.ack=p
                #    self.seq+=1 
            #recieve data from server
            k=self.rdt_recv()
            #assign the recieved data
            self.ack=k
            #increment the count value
            self.count+=1
            data = f'packet is recieved correctly:Ack={self.ack};Seq={self.seq}form:{app_msg_str}.All done!'
            print(data)
            print("count:",self.count)
            print("\n")
            #increment the sequence number by one
            self.seq+=1 
          #if acknowledgement is 0 
          else:
            #if data is a divided by 3
            if(self.count%3==0):
              #if data is divisible by 6
              if(self.count%6==0):
                print("socket timeout! resend!")
                print("\n") 
                print("[timeout retransmission]:",app_msg_str)
                print("packet num.",self.count,"is successfully sent to the reciever.")
                self.count+=1
                #retransmission of data
                p=self.rdt_retransmit(app_msg_str,0,0)   
                self.seq+=1 
                self.ack=p 
                print("\n") 
              #if divisible by 3
              else:
                print("reciever ACK previous packet,resend!")
                print("\n") 
                print("[ACK -previous retransmission]:",app_msg_str)
                print("packet num.",self.count,"is successfully sent to the reciever.")
                self.count+=1
                #retransmission of data by function
                p=self.rdt_retransmit(app_msg_str,0,0)
                self.ack=p
                self.seq+=1  
                print("\n") 
            #if not divisible by 3 or 6
            else:
              print("socket timeout! resend!")
              print("\n") 
              print("[timeout retransmission]:",app_msg_str)
              print("packet num.",self.count,"is successfully sent to the reciever.")
              self.count+=1
              p=self.rdt_retransmit(app_msg_str,0,0)  
              self.ack=p 
              self.seq+=1  
              print("\n") 
        #if the sequence number is 1 enter the next state
        elif(self.seq==1):
          #if the acknowledgement is of zero
          if(self.ack==0):
            app_msg_bytes = app_msg_str.encode('utf-8')
            l = make_packet(app_msg_bytes, self.ack, self.seq)
            print("packet created:",l)
            #sends the data to the server
            self.client_socket.sendto(l, (server_name, server_port))
            print("packet num.",self.count,"is successfully sent to the reciever.")
            k=self.rdt_recv()
            self.ack=k
            self.count+=1
            data = f'packet is recieved correctly:Ack={self.ack};Seq={self.seq}form:{app_msg_str}.All done!'
            print(data)
            print("count:",self.count)
            print("\n") 
            #if the sequence is of 1 when entering into the stage of '1'
            if(self.ack==1):
                self.seq-=1
                self.ack-=1 
            else:
              #if the value divisible by 3
              if(self.count%3==0):
                #if divisible by 6 perform time out
                if(self.count%6==0):
                  print("socket timeout! resend!\n")
                  print("[timeout retransmission]:",app_msg_str)
                  print("packet num.",self.count,"is successfully sent to the reciever.")
                  self.count+=1
                  p=self.rdt_retransmit(app_msg_str,0,1)
                  self.ack=p
                  self.seq-=1
                  print("\n") 
                #divisibles of 3
                else:
                  print("reciever ACK previous packet,resend!\n")
                  print("corrupted")
                  print("[ACK -previous retransmission]:",app_msg_str)
                  print("packet num.",self.count,"is successfully sent to the reciever.")
                  self.count+=1
                  p=self.rdt_retransmit(app_msg_str,0,1)
                  self.ack=p
                  self.seq-=1 
                  print("\n")
              #divisible by other values otherthan 3 and 6 
              else:
                print("socket timeout! resend!\n")
                print("[timeout retransmission]:",app_msg_str)
                print("packet num.",self.count,"is successfully sent to the reciever.")
                self.count+=1
                p=self.rdt_retransmit(app_msg_str,0,1)
                self.ack=p
                self.seq-=1
                print("\n") 
          #if the data recieved is corrupted
          else:  
            app_msg_bytes = app_msg_str.encode('utf-8')
            l = make_packet(app_msg_bytes, self.ack, self.seq)
            print("packet created:",l)
            self.client_socket.sendto(l, (server_name, server_port))
            print("packet num.",self.count,"is successfully sent to the reciever.")
            k=self.rdt_recv()
            self.ack=k
            self.count+=1  
            data = f'packet is recieved correctly:Ack={self.ack};Seq={self.seq}form:{app_msg_str}.All done!'
            print(data)
            print("\n") 
            #if(self.ack==1):
            self.seq-=1
            self.ack-=1 
        else:
          print("Timeout")
          print("socket timeout! resend!")
          sleep(timeout_duration)
          print("[timeout retransmission]:",app_msg_str)
          p=self.rdt_retransmit(app_msg_str,0,0)
          self.ack=p 
          print("p:",self.ack)
          print("\n") 
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """
  #perform receve function to get data from server
  def rdt_recv(self):
    #connection and recieve the data
    message,sever_socket=self.client_socket.recvfrom(2048)
    #decode the recieved data
    k=message.decode()
    decoded_data=int(k)
    ack=decoded_data
    return ack
  #performs retransmission for the data when called
  def rdt_retransmit(self,msg,ack,seq):
    #encode the message to bytes
    app_msg_bytes = msg.encode('utf-8')
    l = make_packet(app_msg_bytes, ack, seq)
    print("packet created:",l)
    #send the packet to the server
    self.client_socket.sendto(l, (server_name, server_port))
    k=self.rdt_recv()
    #data = f'Ack={self.ack};Seq={self.seq}form message to be transmitted:{msg}'
    #print(data)
    #get the acknowledgement
    self.ack=k
    print("\n") 
    #return the recieved acknowledgement
    return self.ack


     
  

  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT change the function name.                    #######                    
  ####### You can have other functions if needed.                             #######   
