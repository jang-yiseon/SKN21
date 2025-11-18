

import my_module #my_module 실행

# my_module의 plus 를 사용하기 위함
result = my_module.plus(10,20)

print(result)

r = my_module.minus(100,300)
print(r)

from my_package import todo_module as todo
# 이렇게 작성해도 가능함

# import my_package.todo_module as todo

#as는 todo로 함축어? 별명? 같은걸로 사용할 수 있게 해줌
# as를 쓰지 않으면 , my_package 같은 경우에는 run.py script와 같은 디렉토리 패키지 안에 존재하여 찾을 수 있음
# 그것을 이용해 같은 패키지 내 디렉토리인 my_package의 todo_module을 찾아내게 하는 것.
# 파일 경로에서 c:/document/ 이런식으로 사용하듯이 python에서는 경로를 설정해줄때 . 으로 설정함

r = todo.print_gugu(6)
#이렇게 as를 쓰는이유는 패키지 말고 script 내에 존재하는 동일 함수를 구분하기 위함임.
# 만약 as 를 사용하지 않은 경우 todo_module.print_gugu하면 됨

