//#define SERVO   6

//char **validacao;


//int PinAnalogLM35 = 0; //Setando Pino A0
//float valAnalog = 0; // Iniciando variavel valAnalog como 0
//float temp = 0; //Iniciando variavel temp como 0

/*struct Mic {
  char text[7];
  char label[10];
  char angleString[3];
  unsigned long angle;
};*/

//Mic micSet [10];



// if (name[count]=='\0')
// {
//    Serial.println (name[1]);
//    stopBit = false;
//    count = 0;
//    i = 0;
//    j = 0;
//  
//    for (k = 3; name[k] != '.'; k++)
//    {
//
//      if (name[k] != ',')
//      {
//        subtexts [i][j] = name[k];
//        j++;
//      }
//      else
//      {
//        j = 0;
//        i++;
//      }
//    }
//    for (i = 0; i < name[1]-'0'; i++)
//    {
//      strcpy(micSet[i].text,subtexts[i]);
//      //Serial.println(subtexts[i]);
//      Serial.println(micSet[i].text);
//    }
//    
//    for (i = 0; i < name[1]-'0';i++)
//    {
//      for (j = 0; micSet[i].text[j] != '['; j++)
//        micSet[i].label[j] = micSet[i].text[j];
//    
//      for (j++, k = 0; micSet[i].text[j] != ']'; j++, k++)
//        micSet[i].angleString[k] = micSet[i].text[j];
//     
//
//      
//      Serial.print(micSet[i].label);
//      Serial.print("\t-\t");
//      Serial.print(micSet[i].angleString);
//      Serial.print("\t-\t");
//      micSet[i].angle = strtoul(micSet[i].angleString, validacao, 10);
//      Serial.println(micSet[i].angle);
//      //micSet[i].angle = atoi (micSet[i].angleString);
////      micSet[i].angle = (micSet[i].angleString.parseInt());
//      //Serial.println(micSet[i].angle);
//       
//    }
//    
//  }
//  
//  
//  s.write(micSet[4].angle);
//
//  
//  
////      Serial.println (name);   
// /*
// if (Serial.available() == 0)
// {
//   aux = 0;
//   micNumbers = 0;
//   while (received[aux] != '.')
//   {
//     if ((received[aux]==',') & (received[aux+1]!=',' & received[aux+1]!='.'))
//     {
//       micNumbers++;
//       Serial.println(micNumbers);
//     }
//     
//   }
// }
//  */
//}