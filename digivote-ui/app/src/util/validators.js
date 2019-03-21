export const required = value => 
  (value === undefined || value === null && value === "")
  ? "Required"
  : undefined;

export const matchFormat = format => value => 
  (value.match(format) === null)
  ? "Invalid Format"
  : undefined;

export const setMessage = (validator, message) => value => 
  validator(value)
  ? message
  : undefined;

export const atLeastN = (n, validators) => value => {
  let count = 0;
  let errors = new Array();
  for (let validator of validators){
    const error = validator(value);
    if(error){
      errors.push(error);
    } else {
      count++;
    }
    if(count >= n){
      return undefined;
    }
  }
  return `At least ${n - count} required: ${errors.join('; ')}`;
}