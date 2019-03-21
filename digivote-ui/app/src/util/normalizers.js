
export const normalizeSSN = (value) => {
  if (value) {
    const onlyNums = value.replace(/[^\d]/g, '')
    if (onlyNums.length <= 3) {
      return onlyNums;
    }
    if (onlyNums.length <= 5) {
      return `${onlyNums.slice(0, 3)}-${onlyNums.slice(3)}`;
    }
    return `${onlyNums.slice(0, 3)}-${onlyNums.slice(3, 5)}-${onlyNums.slice(5, 9)}`;
  }
}

export const normalizePhone = (value) => {
  if(value){
    const onlyNums = value.replace(/[^\d]/g, '')
    if (onlyNums.length <= 3) {
      return onlyNums;
    }
    if (onlyNums.length <= 6) {
      return `${onlyNums.slice(0, 3)}-${onlyNums.slice(3)}`;
    }
    return `${onlyNums.slice(0, 3)}-${onlyNums.slice(3, 6)}-${onlyNums.slice(6, 10)}`;
  }
}