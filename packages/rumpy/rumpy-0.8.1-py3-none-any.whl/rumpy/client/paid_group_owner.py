import time

from rumpy.client import FullNode


class PaidGroupOwner(FullNode):
    def create_group(self, group_name, app_key="group_timeline"):
        """create a paidgroup and announce owner self and approve it"""
        seed_info = self.api.create_group(group_name, consensus_type="poa", encryption_type="private", app_key=app_key)
        self.group_id = seed_info.get("group_id")
        self.seed = seed_info.get("seed")
        # announce owner self and approve it
        resp = self.api.announce_as_user(memo="paidgroup owner")

        for i in range(10):
            if "TrxId" in self.api.get_trx(resp["trx_id"]):
                break
            else:
                time.sleep(0.5)
        resp = self.api.approve_as_user()

        # 充值

        {"group_name": group_name, "consensus_type": "poa", "encryption_type": "private", "app_key": app_key}
        # TODO
        # 创建并把自己
