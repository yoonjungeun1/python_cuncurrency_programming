import asyncio
import time

async def task1():
    print(f"{time.strftime('%X')} - 작업 1 시작")
    await asyncio.sleep(2)  # 2초 대기
    print(f"{time.strftime('%X')} - 작업 1 완료")

async def task2():
    print(f"{time.strftime('%X')} - 작업 2 시작")
    await asyncio.sleep(1)  # 1초 대기
    print(f"{time.strftime('%X')} - 작업 2 완료")

# 여러 코루틴 실행
async def main():
    start_time = time.time()
    await asyncio.gather(task1(), task2())
    print(f"비동기 방식 전체 수행 시간: {time.time() - start_time:.2f} 초")

asyncio.run(main())



def task3():
    print(f"{time.strftime('%X')} - 작업 1 시작")
    time.sleep(2)  # 2초 대기 (동기적 대기)
    print(f"{time.strftime('%X')} - 작업 1 완료")

def task4():
    print(f"{time.strftime('%X')} - 작업 2 시작")
    time.sleep(1)  # 1초 대기 (동기적 대기)
    print(f"{time.strftime('%X')} - 작업 2 완료")

# 여러 작업을 순차적으로 실행
def main():
    start_time = time.time()
    task3()
    task4()
    print(f"동기 방식 전체 수행 시간: {time.time() - start_time:.2f} 초")

main()
