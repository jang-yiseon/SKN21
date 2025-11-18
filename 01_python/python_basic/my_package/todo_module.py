


# 1
def summa(start:int=0, end : int=10) -> int :
    """ 
    start 정수 ~ end 정수까지의 합을 계산하는 함수 
    
    Args : 
        start(int) : 계산 범위의 시작 정수
        end(int) : 계산 범위의 끝 정수
    
    Returns
        int : start ~ end 까지의 모든 정수들의 합계
    """

    result = 0
    for v in range(start, end+1) : 
        result += v
    return result

# print(summa(1,10))

# 2 

# print(summa())

# print(summa(end=20))


# 3

def print_gugu(dan : int) :
    print(f"{dan}단을 출력합니다.")
    for v in range(1,10) : 
        print(f"{dan} x {v} = {dan*v}")

# print_gugu(5)

# def에서 정의할때 print를 사용해서 단을 입력해줄땐 print 사용하면 마지막에 None이 반환됨













# 4. BMI 지수
def check_weight(tall : float, weight : float) -> tuple[float, str] :
    """
    BMI 지수를 계산해서 체중상태를 알려주는 Method
    Args : 
        tall (float) : 키 / 단위 : 미터
        weight (float) : 몸무게 / 단위 : kg

    Returns
        tuple : BMI 지수와 체중상태를 tuple로 묶어서 반환.
    """

    bmi = weight / tall**2 
    result = None
    if bmi < 18.5 :
        result = "저체중"
    elif bmi < 25 :
        result = "정상"
    elif bmi > 25 :
        result = "과체중"
    else : 
        result = "비만"
    return bmi, result

# print(check_weight(1.75, 50.0))


print(__name__) # 모듈이름이 나오는데, 이렇게 todo module에선 본인이 메인이므로 main으로 나옴
if __name__ == "__main__" :  ## 해당 모듈을 다른 모듈에서 사용할 때 원하지 않는 값이 나오지않게하기 위함.
    #메인모듈일 때만 실행함
    print(check_weight(1.75, 50.0))
    print_gugu(7)