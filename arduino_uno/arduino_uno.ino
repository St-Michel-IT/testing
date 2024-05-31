// Install the library from the Arduino IDE library manager
#include <simpleRPC.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  interface(
    Serial,
    floatDivision,
    "floatDivision: Divide the dividend by the divisor. @dividend: float, the dividend. @divisor: float, the dividend.",
    doubleDivision,
    "doubleDivision: Divide the dividend by the divisor. @dividend: double, the dividend. @divisor: double, the dividend.",
    longOverflow,
    "longOverflow: Add an unsigned long to the biggest unsigned long 4294967295.  @toAdd: unsigned long, value to add.",
    isBufferOverflow,
    "isBufferOverflow: Try a possible buffer overflow on the Arduino. @input: Array of bytes. @return: A boolean as flag of probable overflow.");
  // Not much to to after that
}

/*******************************************************************************
 * Function checking ATMega328P Processor and Arduino float precision
 * using a division.
 * Precision should be 32 bits
 * https://www.arduino.cc/reference/en/language/variables/data-types/float/.
 *
 * @param dividend: float, the dividend.
 * @param divisor: float, the divisor.
 * @return float, the result of the division.
 */
float floatDivision(float dividend, float divisor) {
  float result = dividend / divisor;
  return result;
}

/*******************************************************************************
 * Function checking ATMega328P Processor and Arduino double precision
 * using a division.
 * On Arduino Uno, double is the same precision as float according to
 * https://www.arduino.cc/reference/en/language/variables/data-types/double/.
 * So the result should be the same as floatDivision.
 *
 * @param dividend: double, the dividend.
 * @param divisor: double, the divisor.
 * @return double, the result of the division.
 */
double doubleDivision(double dividend, double divisor) {
  double result = dividend / divisor;
  return result;
}

/*******************************************************************************
 * Function checking ATMega328P Processor and Arduino unsigned long overflow
 * protection. According to the Arduino documentation
 * https://www.arduino.cc/reference/en/language/variables/data-types/unsignedlong/
 * those integers are store in 32 bits and therefore range from 0 to 4,294,967,295.
 * Without Overflow protection it should be easy to have a wrong addition result.
 *
 * @param toAdd: An unsigned long to add to 4294967295.
 * @return unsigned long double, the result of the addition.
 */
unsigned long longOverflow(unsigned long toAdd) {
  long result = 4294967295;
  result = toAdd + result;
  return result;
}
/*******************************************************************************
 * Try a possible buffer overflow on the Arduino. Largely inspired by
 * https://hackaday.io/project/174909-simple-security-risk-examples-on-arduino/log/183801-example-1-simple-buffer-overflow
 * It has worked for sure but I don't know how to reproduce it.
 * It probably depends on the memory allocation of the Arduino.
 * At least it shows that the Arduino is not protected against buffer overflow
 * if the input is not checked and long enough to overflow the buffer.
 *
 * @param byte: Array of bytes.
 * @return A boolean as flag of probable overflow.
 */
bool isBufferOverflow(byte input[]) {
  char buff[16] = { 0 };
  // How and when this variable can be modified?
  uint8_t unlocked_flags[32] = { 0 };

  // Loop over the input using a for loop
  for (int i = 0; i < sizeof(input); i++) {
    buff[i] = input[i];
  }

  if (unlocked_flags[0]) {
    return true;
  } else {
    return false;
  }
}