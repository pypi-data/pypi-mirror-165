**Features**
============

  A simulation of the historic enigma machine, covering its flaws and
  improving the scope of the technique.   
  1. Adding to the original Enigma, this technique can accept most
  characters, numbers and even spaces in the key. 
  2. Each character in the string is capable of being encrypted unlike
  the original edition. 
  3. The key length is not limited to just 5, as
  in a usual enigma machine, the user can create any n length key 
  4. Alphabets, characters and even empty spaces are encrypted in this
  technique and the key can also have empty spaces as a character !

To decrypt a message enter the decrypted message and use the same key
length and key used for encryption

**Usage**
=========

The module is easy to use. To use the module after installing it, write
the following code-

*From Multi_Rotor_Enigma import Multi_Rotor_Enigma  
print(Multi_Rotor_Enigma.Encrypt(msg,no. of rotors,key))*

There is the main function Enigma which has 3 attributes- they are (in
order)

**Message to encrypt (string)**

**Number of rotors user wants (integer)**

**Setting of rotors (string)**

Note- The length of setting and number of rotors should be the same
otherwise an error will occur

**Example**
===========

  Let’s quickly see with an example how the module works. For example if
  we have to encrypt the string, ‘hello world’ with 6 rotors and using
  the key as#wr% I shall write  
  *import Multi_Rotor_Enigma  
  print(Multi_Rotor_Enigma.Multi_Rotor_Enigma.Enigma(‘hello
  world’,6,‘as#wr%’))*

For decryption, I repeat the same process, just that the message to
decrypt will replace the ‘hello world’ part while the key length and
number of rotors combination will remain the same as used during the
encryption part.
