from socket import *
from util import *
from time import sleep
## No other imports allowed
server_port=10516
#create socket
server_socket=socket(AF_INET, SOCK_DGRAM) 
#bind the socket
server_socket.bind(('',server_port))
#connection of UDP established
print('The UDP server is ready to receive..')
#initialized all the values
count=1 
timeout_duration=3
data=0
#create a function to take module 3 values
def mod3():
    if(count%3==0):
                #some elements might also be divisble by both 3 and 6
                if(count%6==0):
                    print("simulating packet loss:sleep a while to trigger timeout event on the send side...")
                    sleep(timeout_duration)    
                else:
                    print("simulating packet bit errors/corrupted:Ack the previous packet..")
#function for modulus of 6                    
def mod6():
    print("simulating packet loss:sleep a while to trigger timeout event on the send side...")
    sleep(timeout_duration)           
with open("received_pkt.txt", "wb") as file:
    while True:   
        msg,client_socket=server_socket.recvfrom(1024)
        print("packet num.",count,"received:",msg)
        file.write(msg+ b"\n")
        # Separate the components without changing the data type
        string1_bytes = msg[:8]  # 'COMPNETW' as bytes
        hex_data_bytes = msg[8:10]  # '\xf7\xde' as bytes
        string2_bytes = msg[10:]  # '\x00@msg1' as bytes
        string3_bytes=msg[12:]     #b'msg1'
        #verify the data recieved was correct or wrongly recieved
        check=verify_checksum(hex_data_bytes,string2_bytes)
        #if the data recieved correctly
        if(check==True):
            #get the sequence number from the given data packet
            seq=extract_sequence_number(msg)
            #if the sequence number 0 sends the acknowledgement 0
            if(seq==0):
                if(count%3==0):
                    mod3()
                    l=1
                    data=str(l)
                    server_socket.sendto(data.encode(), client_socket)    
                elif(count%6==0):
                    mod6()
                    l=1
                    data=str(l)
                    server_socket.sendto(data.encode(), client_socket)
                else:
                    l=0
                    data=str(l)
                    print("packet is delivered,now creating and sending the ACK packet...")
                    print("packet is expected, message string delivered:",string3_bytes)
                    server_socket.sendto(data.encode(), client_socket)
            #if sequence number is 1 then send acknowledgement 1
            else:
                if(count%3==0):
                    mod3()
                    l=0
                    data=str(l)
                    print("packet is delivered,now creating and sending the ACK packet...")
                    server_socket.sendto(data.encode(), client_socket)    
                elif(count%6==0):
                    mod6()
                    l=0
                    data=str(l)
                    print("packet is delivered,now creating and sending the ACK packet...")
                    server_socket.sendto(data.encode(), client_socket)
                else:
                    l=1
                    data=str(l)
                    print("packet is delivered,now creating and sending the ACK packet...")
                    print("packet is expected, message string delivered:",string3_bytes)
                    server_socket.sendto(data.encode(), client_socket)
            count+=1
         #if the received data is corrupted   
        else:
            #Extract sequence number from the packet
            seq=extract_sequence_number(msg)
            #if sequence number is 0 send acknowledgement 1 because it is corrupted
            if(seq==0):
                l=1
                data=str(l)
                server_socket.sendto(data.encode(), client_socket)
            #if sequence number is 1 send acknowledgement 0 because it is corrupted
            else:
                l=0
                data=str(l)
                server_socket.sendto(data.encode(), client_socket)
            #increase the count value
            count+=1
            print("simulating packet bit errors/corrupted:Ack the previous packet..")
        print("all done for this packet!")
        print("\n")
