kill @e
scoreboard players add @p[tag=printing] printcool 1
execute @p[scores={printcool=20..},tag=printing] ~~~ scoreboard players add @s print 1
execute @p[scores={printcool=20..},tag=printing] ~~~ function print
execute @p[scores={printcool=20..},tag=printing] ~~~ scoreboard players set @s printcool 0