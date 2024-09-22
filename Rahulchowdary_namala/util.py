def create_checksum(packet_wo_checksum):
    # Initialize the checksum to 0
    value = b'COMPNETW\x00\x00'  # Existing byte string
    new_data = packet_wo_checksum  # The new data you want to add

    # Concatenate the new data to the existing byte string
    value = value + new_data
    # Print the updated byte string
    checksum = 0

    # Calculate the checksum
    for i in range(0, len(value), 2):
      if i + 1 < len(value):
      # Get two bytes as a 16-bit word
          data_word = value[i] << 8 | value[i + 1]
      else:
         data_word = (value[i] << 8)
      checksum += data_word

    # Fold the carry bits
    while (checksum >> 16) > 0:
      checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # Take the one's complement of the result
    checksum = ~checksum & 0xFFFF

    # Convert the 16-bit checksum to a bytes object
    checksum_bytes = checksum.to_bytes(2, byteorder='big')

    # Print the checksum as a bytes object
    return(checksum_bytes)
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """

def verify_checksum(packet, msg):
    # Extract the received checksum bytes from the packet
    received_checksum_bytes = packet[0:8]
    # Convert the received checksum bytes to a 16-bit integer
    received_checksum = int.from_bytes(received_checksum_bytes, byteorder='big')
    # Initialize the checksum to 0
    checksum = 0
    value = b'COMPNETW'
    # Calculate the checksum for the packet data, excluding the received checksum
    byte_string = value+b'\x00\x00' + msg
    for i in range(0, len(byte_string), 2):
        if i + 1 < len(byte_string):
            data_word = (byte_string[i] << 8) | byte_string[i + 1]
        else:
            data_word = (byte_string[i] << 8)
        checksum += data_word

    # Add the received checksum to the calculated checksum
    #checksum += received_checksum
    # Fold the carry bits
    while (checksum >> 16) > 0:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # Take the one's complement of the result
    checksum = ~checksum & 0xFFFF

    # If the final checksum matches the received checksum, the packet is valid
    is_valid = checksum == received_checksum
    # Return result
    if is_valid:
      return(True)
    else:
        return(False)
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

  Args:
    packet: the whole (including original checksum) packet byte data

  Returns:
    True if the packet checksum is the same as specified in the checksum field
    False otherwise

  """

def make_packet(data_str, ack_num, seq_num):
    header=8+4+len(data_str)
    packet_length_binary = format(header, '014b')
    packet_length_binary+=str(ack_num)
    packet_length_binary+=str(seq_num)
    #Here the length of packets
    packet_length_int = int(packet_length_binary, 2)
    #Here it creates data \00@
    packet_length_bytes = packet_length_int.to_bytes(2, byteorder='big')
    #Here it is in the format \x00@msg1
    combine_message=packet_length_bytes+data_str
    #gets the checksum \xf7\xde
    check_sum=create_checksum(combine_message)
    #final output b'COMPNETW\xf7\xde\x00@msg1'
    final_packet=b"COMPNETW"+check_sum+combine_message
    return(final_packet)
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    # make sure your packet follows the required format!
def extract_sequence_number(packet):
    if len(packet) < 12:
        return None  # Packet is too short to contain sequence number

    # Assuming the sequence number is a single character at the 12th position
    sequence_number = packet[11] # Extract and decode the character
    if(sequence_number==66 ):
      sequence=0
    elif (sequence_number==67):
      sequence=1
    elif(sequence_number==64):
      sequence=0
    elif(sequence_number==65):
      sequence=1
    else:
      sequence=0
    return sequence


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  