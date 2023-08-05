from gssc.networks import ResSleep, SleepGRU
from gssc.utils import make_blueprint
import torch

sigs = {"eeg":{"chans":"eeg", "perms":[0,1], "flip":True},
        "eog":{"chans":"eog", "perms":[0,1], "flip":True}}
blueprints = {}
blueprints["eog"] = make_blueprint(4, 8, 10, None, 0)
blueprints["eeg"] = make_blueprint(4, 8, 10, 2, 4)

net = ResSleep(list(sigs.keys()), blueprints, 5, 5,
               {"eeg":[512], "eog":[512], "eeg eog":[1024, 512, 512]},
               fc_dec=[512, 512, 512], norm=True, dropout=0.5)
gru_net = SleepGRU(512, 256, 5, 5, bidirectional=True, norm=True, dropout=0.5)

net_type = "gru"
net_dir = "gru_4deep"
net_inds = [14, 15, 17]


root_dir = "/home/jev/"
res_dir = root_dir + "deepsleep/results/{}/".format(net_dir)
yasa_out_dir = root_dir + "deepsleep/results/"

# average weights if multiple net_inds given
res_weights = [torch.load("{}net_state_{}.pt".format(res_dir, net_idx))
               for net_idx in net_inds]
for key in res_weights[0]:
    res_weights[0][key] = sum([x[key] for x in res_weights]) / len(res_weights)
con_weights = [torch.load("{}{}_net_state_{}.pt".format(res_dir, net_type, net_idx))
               for net_idx in net_inds]
for key in con_weights[0]:
    con_weights[0][key] = sum([x[key] for x in con_weights]) / len(con_weights)

net.load_state_dict(res_weights[0])
gru_net.load_state_dict(con_weights[0])

torch.save(net, "nets/sig_net_v1.pt")
torch.save(gru_net, "nets/gru_net_v1.pt")
