# xend_cooperative = xend.personal.get_flexible_deposit_record()

from xend_finance import XendFinance

xend = XendFinance(56,'0x06cce0427cbdd1e46197477124e41e0ba018f3153dc8a60015fdf656c325c011', {"env": "local"})

#  COOPERATIVE


# args = {
#     "group_id": 1,
#     "cycle_stake_amount": "0.1",
#     "payout_interval_in_seconds": 3600,
#     "start_time_in_seconds": 1579014400,
#     "max_members": 10
# }
# create_cooperate = xend.cooperative.create(args)
# print(create_cooperate)


# # args = {
# #     "group_id": 1,
# #     "cycle_stake_amount": "0.1",
# #     "payout_interval_in_seconds": 3600,
# #     "start_time_in_seconds": 1579014400,
# #     "max_members": 10
# # }
# join_cooperative = xend.cooperative.join(10,25)
# print(join_cooperative)

# cooperative_cycle_info = xend.cooperative.info(5)
# print(cooperative_cycle_info)

# does_member_exist = xend.cooperative.cycle_member_exist(5)
# print(does_member_exist)

# start_cycle = xend.cooperative.start_cycle(3)
# print(type(start_cycle))

# withdraw_ongoing_cycle = xend.cooperative.withdraw_from_ongoing_cycle(1)
# print(withdraw_ongoing_cycle)

# withdraw_completed_cycle = xend.cooperative.withdraw_completed(1)
# print(withdraw_completed_cycle)

# create_cooperative_group = xend.cooperative.create_group('test', 'TST')
# print(create_cooperative_group)

# get_cooperative_groups = xend.cooperative.get_cooperative_groups()
# print(get_cooperative_groups)

# cooperative_cycles_contributions = xend.cooperative.contributions()
# print(cooperative_cycles_contributions)

# cycles_in_cooperative_group = xend.cooperative.cycles_in_group(1)
# print(cycles_in_cooperative_group)

# # ESUSU


# args = {
#     "group_id": 1,
#     "deposit_amount": "300",
#     "payout_interval_in_seconds": 3600,
#     "start_time_in_seconds": 1579014400,
#     "max_members": 10
# }
# create_esusu_cycle = xend.esusu.create_esusu(args)
# print(create_esusu_cycle)

# get_esusu_cycles_count = xend.esusu.get_cycles_count()
# print(get_esusu_cycles_count)

# get_esusu_cycle_id = xend.esusu.get_cycle_id_from_cycles_created(6)
# print(get_esusu_cycle_id)

# get_esusu_info = xend.esusu.get_esusu_info(5)
# print(get_esusu_info)

# join_esusu_cycle = xend.esusu.join(9)
# print(join_esusu_cycle)

# start_esusu_cycle = xend.esusu.start(3)
# print(start_esusu_cycle)

# withdraw_interest = xend.esusu.withdraw_interest(8)
# print(withdraw_interest)

# withdraw_capital = xend.esusu.withdraw_capital(14)
# print(withdraw_capital)

# is_member_of_esusu_cycle = xend.esusu.is_member_of_cycle(9)
# print(is_member_of_esusu_cycle)

# get_interest_capital = xend.esusu.accrue_interest_capital(16)
# print(get_interest_capital)

# create_esusu_group = xend.esusu.create_group('test', 'TXT')
# print(create_esusu_group)

# get_esusu_group = xend.esusu.get_groups()
# print(get_esusu_group)

# no_of_contributions = xend.esusu.no_of_contributions()
# print(no_of_contributions)

# esusu_contributions = xend.esusu.contributions()
# print(esusu_contributions)

# esusu_cycles_in_group = xend.esusu.cycles_in_group(11)
# print(esusu_cycles_in_group)


# # GROUP
# create_group = xend.group.create('mnt', 'MNT')
# print(create_group)

# get_single_group = xend.group.get_single_group(1)
# print(get_single_group)

# get_groups = xend.group.get_groups()
# print(get_groups)

# get_xend_rewards = xend.group.get_xend_rewards()
# print(get_xend_rewards)

# # PERSONAL
# create_flexible_deposit = xend.personal.flexible_deposit("20")
# print(create_flexible_deposit)

# create_fixed_deposit = xend.personal.fixed_deposit(40, 30)
# print(create_fixed_deposit)

# fixed_deposit_record = xend.personal.get_fixed_deposit_record()
# print(fixed_deposit_record)

# flexible_deposit_record = xend.personal.get_flexible_deposit_record()
# print(flexible_deposit_record)

# fixed_withdrawal = xend.personal.fixed_withdrawal(10)
# print(fixed_withdrawal)

# flexible_withdrawal = xend.personal.flexible_withdrawal(30)
# print(flexible_withdrawal)

# # XAUTO

# approve_token = xend.xauto.approve("TNT", 300)
# print(approve_token)

# deposit_token = xend.xauto.deposit("BSC",150)
# print(deposit_token)

# deposit_native_token = xend.xauto.deposit_native("DAI", 300)
# print(deposit_native_token)

# withdraw_token = xend.xauto.withdraw("DAI",240)
# print(withdraw_token)

# get_ppfs = xend.xauto.ppfs("DAI")
# print(get_ppfs)

# get_share_balance = xend.xauto.share_balance("DAI")
# print(get_share_balance)

# # XVAULT

# approve_token = xend.xvault.approve("BSC", 250)
# print(approve_token)

# deposit_token = xend.xvault.deposit("BSC",150)
# print(deposit_token)

# withdraw_token = xend.xvault.withdraw("DAI",240)
# print(withdraw_token)

# get_ppfs = xend.xvault.ppfs("DAI")
# print(get_ppfs)

# get_share_balance = xend.xvault.share_balance("DAI")
# print(get_share_balance)

# GENERAL

# create_wallet = xend.create_wallet()
# print(create_wallet)

# retrieve_wallet = xend.retrieve_wallet()
# print(retrieve_wallet)

# wallet_balance = xend.wallet_balance()
# print(wallet_balance)

# get_ppfs = xend.get_ppfs()
# print(get_ppfs)