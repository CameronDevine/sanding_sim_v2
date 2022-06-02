.PHONY: all bam clean eggs

blend_files = $(wildcard *.blend)
bam_files = $(blend_files:.blend=.bam)

all: bam eggs

clean:
	ls | grep "^[0-9,a-f].*\.json" | xargs rm

bam: $(bam_files)

%.bam: %.blend
	blend2bam $< $@

eggs: buttons.egg radio.egg

buttons.egg: button.png button_pressed.png button_disabled.png
	egg-texture-cards -o $@ -g -2,2,-0.72,0.72 -p 189,68 $^

radio.egg: radio.png radio_checked.png
	egg-texture-cards -o $@ -g -1,1,-0.72,0.72 -p 85,61 $^
