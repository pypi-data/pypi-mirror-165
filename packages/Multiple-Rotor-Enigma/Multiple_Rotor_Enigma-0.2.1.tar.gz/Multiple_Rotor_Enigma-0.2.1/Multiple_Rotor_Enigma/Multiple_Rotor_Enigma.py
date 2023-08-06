def Enigma(msg_to_enc,num_of_rotors,setting):
    numero = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12,
              'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17,
              'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,'1':27,'2':28,'3':29 ,'4':30,
               '5':31 , '6':32,'7':33, '8':34 ,'9':35, '0':36 , '!':37, '"':38,r"'":39, '#':40,'$':41 ,'%':42,' ':43,'&':44,
               '*':45, '(':46,')':47, '@':48, '+':49,',':50,'-':51,'.':52,'/':53,';':54,':':55,'>':56,'<':57,'=':58,'[':59,
              ']':60,'_':61,'{':62,'}':63}
    def plugboard(letter):
       initi = ['A','}', '{', '_', ']', '[', '=', '<', '>', ':', ';', '/', '.', '-', ',', '+', '@', ')', '(', '*', '&',
                   ' ', '%', '$', '#', "'", '"', '!', '0', '9', '8', '7', '6', '5', '4', '3', '2', '1','Z',
                   'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H',
                   'G',
                   'F', 'E', 'D', 'C', 'B']
       elem = initi.index(letter)
       return initi[62-elem]

    def rotor_end(rotor_in):
        j = 0
        rotor_1_out = []
        for num in rotor_in:
            a = rotor_in.index(j)
            rotor_1_out.append(a)
            j += 1
        return rotor_1_out

    def rot_move(rotor):
        rotor = rotor[len(numero)-1:] + rotor[0:len(numero)-1]
        return rotor

    def rot_out_move(rotor_in):
        j = 0
        rotor_out = []
        for num in rotor_in:
            a = rotor_in.index(j)
            rotor_out.append(a)
            j += 1
        return rotor_out

    temp = 0
    while temp != 1:
        rotor_0 = ['A','}', '{', '_', ']', '[', '=', '<', '>', ':', ';', '/', '.', '-', ',', '+', '@', ')', '(', '*', '&',
                   ' ', '%', '$', '#', "'", '"', '!', '0', '9', '8', '7', '6', '5', '4', '3', '2', '1','Z',
                   'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H',
                   'G',
                   'F', 'E', 'D', 'C', 'B']
        temm = 0

        rotor_in = {}
        mid_in = [21, 20, 16, 25, 18, 22, 10, 12, 17, 11, 6, 9, 7, 15, 19, 13, 2, 8, 4, 14, 1, 0, 5, 24, 23, 3, 31, 38, 34,
                  33, 40, 26, 51, 29, 28, 55, 46, 59, 27, 43, 30, 54, 61, 39, 58, 50, 36, 60, 49, 48, 45, 32, 52, 56, 41,
                  35, 53, 57, 44, 37, 47, 42, 62]
        rotor_in['rotor_{0}_in'.format(num_of_rotors + 1)] = mid_in
        #rotor_0_in = [2, 0, 3, 9, 20, 5, 6, 14, 16, 15, 1, 18, 8, 25, 13, 11, 21, 24, 4, 17, 10, 12, 19, 23, 7, 22,27,28,26]
        rotor_0_in = [1, 7, 5, 23, 24, 25, 10, 18, 9, 15, 0, 11, 4, 16, 12, 2, 22, 20, 17, 6, 3, 8, 14, 13, 21, 19, 43, 54,
                      44, 35, 56, 30, 26, 55, 46, 47, 53, 59, 51, 27, 31, 41, 39, 61, 32, 50, 29, 62, 34, 37, 57, 60, 36,
                      33, 48, 40, 42, 58, 38, 45, 49, 28, 52]
        rotor_0_out = [10, 0, 15, 20, 12, 2, 19, 1, 21, 8, 6, 11, 14, 23, 22, 9, 13, 18, 7, 25, 17, 24, 16, 3, 4, 5, 32,
                       39, 61, 46, 31, 40, 44, 53, 48, 29, 52, 49, 58, 42, 55, 41, 56, 26, 28, 59, 34, 35, 54, 60, 45, 38,
                       62, 36, 27, 33, 30, 50, 57, 37, 51, 43, 47]
        rotor_in['rotor_0_in'] = rotor_0_in
        gen = {}
        gen_1_in = [20, 23, 13, 2, 8, 7, 19, 5, 9, 25, 15, 12, 17, 6, 21, 24, 10, 22, 4, 1, 3, 14, 16, 0, 18, 11, 33, 49,
                    36, 51, 46, 39, 56, 41, 37, 27, 58, 47, 61, 57, 30, 43, 53, 28, 54, 42, 55, 32, 26, 48, 34, 50, 62, 31,
                    52, 45, 44, 59, 60, 38, 29, 40, 35]
        gen_2_in = [22, 0, 6, 14, 16, 2, 18, 8, 21, 5, 9, 19, 4, 7, 24, 25, 10, 17, 20, 1, 11, 15, 23, 12, 3, 13, 58, 52,
                    36, 33, 48, 32, 43, 45, 47, 38, 35, 29, 62, 61, 57, 50, 28, 56, 44, 51, 55, 39, 49, 60, 54, 46, 27, 40,
                    37, 59, 41, 34, 30, 26, 42, 31, 53]
        gen_0_in = [1, 19, 22, 23, 8, 6, 10, 17, 24, 15, 9, 21, 11, 7, 20, 25, 14, 13, 16, 4, 0, 5, 12, 18, 2, 3, 51, 29,
                    34, 45, 59, 55, 35, 41, 30, 52, 43, 40, 50, 39, 47, 33, 27, 44, 31, 37, 42, 53, 54, 38, 57, 32, 46,
                    58, 48, 62, 56, 36, 26, 28, 60, 61, 49]
        gen['gen_1_in'] = gen_1_in
        gen['gen_2_in'] = gen_2_in
        gen['gen_0_in'] = gen_0_in
        rotor_out = {}
        rotor_out["rotor_0_out"] = rotor_0_out
        setting = setting.upper()
        temp = 0
        while temp == 0:
            if len(setting) == num_of_rotors:
                temp = 1
                futures = list(setting)
                future = []
                check = []
                for letttt in futures:
                    future.append(numero[letttt])
                    check.append('0')
            else:
                return (
                    'Length of setting should match with the number of rotors.Also no space should be left between characters.'
                    ' Please try again')
        temp = 0
        rotor = {}
        rotor['rotor_0'] = rotor_0
        for i in range(0, len(setting)):
            position = list(setting)[i]
            rotor["rotor_{0}".format(i + 1)] = rotor_0[rotor_0.index(position):len(numero)+1] + rotor_0[0:rotor_0.index(position)]
        for i in range(0, len(setting)):
            position = list(setting)[i]
            rotor_in["rotor_{0}_in".format(i + 1)] = gen["gen_{0}_in".format(i % 3)][rotor_0.index(position):len(numero)+1] + gen[
                                                                                                                       "gen_{0}_in".format(
                                                                                                                           i % 3)][
                                                                                                                   0:rotor_0.index(
                                                                                                                       position)]
            rotor_out["rotor_{0}_out".format(i + 1)] = rotor_end(rotor_in["rotor_{0}_in".format(i + 1)])

        bef = {}
        nooo = 0
        ENC = []
        for letter in msg_to_enc:
                     if letter.upper() in rotor_0:
                        try:
                            letter=letter.upper()
                        except:
                            letter=letter
                        nooo += 1
                        letter=plugboard(letter)
                        bef['bef_r0'] = letter
                        for l in range(0, (num_of_rotors)):
                            bef["bef_r{0}".format(l + 1)] = rotor["rotor_{0}".format(l + 1)][
                                rotor_in["rotor_{0}_in".format(l)][
                                    rotor["rotor_{0}".format(l)].index(bef["bef_r{0}".format(l)])]]
                        bef["bef_r{0}".format(num_of_rotors + 1)] = rotor_0[rotor_in["rotor_{0}_in".format(num_of_rotors)][
                            rotor["rotor_{0}".format(num_of_rotors)].index(bef["bef_r{0}".format(num_of_rotors)])]]
                        bef["bef_r{0}".format(num_of_rotors + 2)] = rotor_0[
                            rotor_in["rotor_{0}_in".format(num_of_rotors + 1)][
                                rotor_0.index(bef["bef_r{0}".format(num_of_rotors + 1)])]]
                        bef["bef_r{0}".format(num_of_rotors + 3)] = rotor["rotor_{0}".format(num_of_rotors)][
                            rotor_out["rotor_{0}_out".format(num_of_rotors)][
                                rotor_0.index(bef["bef_r{0}".format(num_of_rotors + 2)])]]
                        for p in reversed(range(0, (num_of_rotors))):
                            bef["bef_r{0}".format((2 * num_of_rotors) + 3 - p)] = rotor["rotor_{0}".format(p)][
                                rotor_out["rotor_{0}_out".format(p)][
                                    rotor["rotor_{0}".format(p + 1)].index(
                                        bef["bef_r{0}".format((2 * num_of_rotors) + 2 - p)])]]

                        ENC.append(plugboard(bef["bef_r{0}".format((2 * (num_of_rotors + 2)) - 1)]))

                        rotor["rotor_{0}".format(1)] = rot_move(rotor["rotor_{0}".format(1)])
                        rotor_in["rotor_{0}_in".format(1)] = rot_move(rotor_in["rotor_{0}_in".format(1)])
                        rotor_out["rotor_{0}_out".format(1)] = rot_out_move(rotor_in["rotor_{0}_in".format(1)])
                        for m in range(1, num_of_rotors):
                            if check[m] == '0':
                                if ((len(numero)+1) * m) - (sum(future[0:m])) == nooo:
                                    rotor["rotor_{0}".format(m)] = rot_move(rotor["rotor_{0}".format(m)])
                                    rotor_in["rotor_{0}_in".format(m)] = rot_move(rotor_in["rotor_{0}_in".format(m)])
                                    rotor_out["rotor_{0}_out".format(m)] = rot_out_move(
                                        rotor_in["rotor_{0}_in".format(m)])
                                    check[m] = '1'
                                    break
                            else:
                                rotor["rotor_{0}".format(m)] = rot_move(rotor["rotor_{0}".format(m)])
                                rotor_in["rotor_{0}_in".format(m)] = rot_move(rotor_in["rotor_{0}_in".format(m)])
                                rotor_out["rotor_{0}_out".format(m)] = rot_out_move(rotor_in["rotor_{0}_in".format(m)])
                     else:
                            ENC.append(letter)

        enc = ''.join(ENC)
        return enc

