.PHONY: all bam clean

blend_files = $(wildcard *.blend)
bam_files = $(blend_files:.blend=.bam)

all: bam

clean:
	ls | grep "^[0-9,a-f].*\.json" | xargs rm

bam: $(bam_files)

%.bam: %.blend
	blend2bam $< $@
