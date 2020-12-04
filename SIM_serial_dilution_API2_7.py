# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:17:18 2020

@author: marya
"""

from opentrons import simulate

metadata = {'apiLevel': '2.8'}
protocol = simulate.get_protocol_api('2.8')


plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
p300 = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_1])
reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 3)

# reservoir A1 is stock solution
# reservoir A2 is PBS
# reservoir 3 is trash


# distribute PBS: 100ul from reservoir A2 to row A and columns 2-12

p300.distribute(100, reservoir.wells('A2'),plate.rows()[0][1:12])

# distribute stock: 100ul from reservoir A1 to row A and columns 1-2
p300.distribute(100, reservoir.wells('A1'),plate.rows()[0][0:2])

for j in range(1,10):
    p300.transfer(100, plate.columns()[j], plate.columns()[j+1], mix_before=(2, 50), blowout_location='destination well', touch_tip=True, blow_out=True, new_tip='always')    

p300.transfer(100, plate.columns()[10], reservoir.wells('A3'), mix_before=(2, 50), blowout_location='destination well', touch_tip=True, blow_out=True, new_tip='always') 
   
for line in protocol.commands(): 
        print(line)