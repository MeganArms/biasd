all: biasd_c biasd_cuda

biasd_c: ./src/biasd_c.c ./src/biasd_c.h
	mkdir -p lib
	gcc -shared -fPIC -O3 -o ./lib/biasd_c.so ./src/biasd_c.c -lm

biasd_cuda: ./src/biasd_cuda.cu
	mkdir -p lib
	nvcc --relocatable-device-code=true --compiler-options '-fPIC' -D_FORCE_INLINES -Xcompiler "-O3" -o ./src/biasd_cuda_integrate.o -c ./src/biasd_cuda_integrate.cu
	nvcc --shared --relocatable-device-code=true --compiler-options '-fPIC' -D_FORCE_INLINES -Xcompiler "-O3" -o ./lib/biasd_cuda.so ./src/biasd_cuda.cu ./src/biasd_cuda_integrate.o
	rm ./src/biasd_cuda_integrate.o

clean:
	rm -rf ./lib
