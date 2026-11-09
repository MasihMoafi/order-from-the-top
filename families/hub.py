"""All communications go through the packet hub."""

from .tree import edge


class Hub:
    def __init__(self, agents, log, counter=0):
        self.agents, self.log, self.counter = agents, log, counter
        self.inbox = {a: [] for a in agents}
        self.open_family = False  # growth worlds: the open-channel arm
        self.channels = set()  # pairs of agents that built a channel themselves

    def send(
        self,
        rnd,
        sender,
        receiver,
        content,
        messenger=False,
        partner=False,
        anonymous=False,
        order=None,
    ):
        self.counter += 1
        relation = (
            "messenger"
            if messenger
            and sender in self.agents
            and receiver in self.agents
            and sender != receiver
            else "partner"
            if partner
            else edge(self.agents, sender, receiver, self.open_family)
            or ("channel" if frozenset((sender, receiver)) in self.channels else None)
        )
        reason = None
        if not relation:
            reason = "edge not permitted"
        elif not self.agents[sender]["alive"] or not self.agents[receiver]["alive"]:
            reason = "sender or receiver dead"
        packet = {
            "id": f"m{self.counter:08d}",
            "round": rnd,
            "sender": sender,
            "receiver": receiver,
            "edge": relation,
            "content": content,
            "delivered": reason is None,
            "reason": reason,
        }
        if order in ("C", "D") and edge(self.agents, sender, receiver) == "child":
            packet["order"] = order
        self.log("packet", **packet)
        if reason is None:
            self.inbox[receiver].append(
                {**packet, "sender": "a member of another family"}
                if anonymous
                else packet
            )
        return packet

    def letter(self, rnd, sender, receiver, text, context_id):
        content = {
            "role": "agent",
            "parts": [{"kind": "text", "text": text}],
            "messageId": f"m{self.counter + 1:08d}",
            "contextId": context_id,
        }
        return self.send(rnd, sender, receiver, content)
