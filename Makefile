.PHONY: all bam

blend_files = $(wildcard *.blend)
bam_files = $(blend_files:.blend=.bam)

all: bam

bam: $(bam_files)

%.bam: %.blend
	blend2bam $< $@
