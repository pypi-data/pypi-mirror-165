from datetime import datetime
import visdom
import torch


class Classification_Visualiser:
    def __init__(self, env_name=None, host='http://localhost', port=8097):
        if env_name is None:
            env_name = str(datetime.now().strftime('%d-%m-%Hh%M'))
        self.env_name = env_name
        self.vis = visdom.Visdom(server=host, port=port, env=self.env_name)
        self.loss_win = None
        self.acc_win = None
        self.text_win = None

    def plot_loss(self, loss, epoch):
        self.loss_win = self.vis.line(
            [loss], [epoch],
            win=self.loss_win, update='append' if self.loss_win else None,
            opts={
                'xlabel': 'Epoch',
                'ylabel': 'Loss',
                'legend': ['train', 'test'],
                'layoutopts': {
                    'legend': {
                        'train': 0,
                        'test': 1
                    }
                }
            }
        )

    def plot_accuracy(self, acc, epoch):
        self.acc_win = self.vis.line(
            [acc], [epoch],
            win=self.acc_win, update='append' if self.acc_win else None,
            opts={
                'xlabel': 'Epoch',
                'ylabel': 'Accuracy',
                'legend': ['train', 'test'],
                'layoutopts': {
                    'legend': {
                        'train': 0,
                        'test': 1
                    }
                }
            }
        )

    def show_text(self, text):
        self.text_win = self.vis.text(
            text, win=self.text_win
        )


def train_classifier(model, criterion, optimiser, epochs, visualiser, loaders, sizes, device='cpu'):
    model = model.to(device)
    losses = {
        'train': None,
        'test': None
    }
    acc = {
        'train': None,
        'test': None
    }
    for epoch in range(epochs):
        text = '<h2> Epoch %d / %d </h2><br/><br/>' % (epoch + 1, epochs)

        for stage in ['train', 'test']:
            if stage == 'train':
                model.train()
            else:
                model.eval()

            running_loss = .0
            running_correct = 0

            for input, label in loaders[stage]:
                input, label = input.to(device), label.to(device)
                optimiser.zero_grad()

                with torch.set_grad_enabled(stage == 'train'):
                    output = model(input)
                    _, pred = torch.max(output, 1)
                    loss = criterion(output, label)

                    if stage == 'train':
                        loss.backward()
                        optimiser.step()

                    running_loss += loss.item() * input.size(0)
                    running_correct += torch.sum(pred == label.data)

            stage_loss = running_loss/sizes[stage]
            stage_accuracy = running_correct.double() / sizes[stage]

            losses[stage] = stage_loss
            acc[stage] = stage_accuracy.cpu().numpy()

            text += '<strong> %s  Loss: </strong> %.3f <strong> Acc: </strong> %.3f <br/><br/>' % \
                    (stage, stage_loss, stage_accuracy)

        visualiser.plot_loss(list(losses.values()), [epoch, epoch])
        visualiser.plot_accuracy(list(acc.values()), [epoch, epoch])
        visualiser.show_text(text)
