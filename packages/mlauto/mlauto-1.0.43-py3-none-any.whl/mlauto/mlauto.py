import torch
import torchvision
import matplotlib.pyplot as plt
import numpy as np
random_seed = 1
torch.backends.cudnn.enabled = False
torch.manual_seed(random_seed)
from scipy.signal import savgol_filter

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os

import socket
import pickle, json

def send_data_to_db(data):
  host = '127.0.0.1'  # Standard loopback interface address         
  port = 6000       # Port to listen on (non-privileged ports are > 1023)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((host, port))

  from_server = client.recv(4096)
  print(from_server)

  json_str = json.dumps(data)
  json_str += 'EOD'
  
  data = json_str.encode('utf-8')

  client.sendall(data) #a bytes-like object is required, not 'str'

  from_server = client.recv(4096)
  print(from_server)
  
  return from_server.decode("utf-8")
  #return '1'


def login(username, key):
  print("Logging in...")
  credentials = {'username':username, 'key':key, 'task':'login'}
  db_answer = send_data_to_db(credentials)
  
  if db_answer == '1':
    os.environ["username"] = username
    os.environ["key"] = key
    print("Logged in successfully!")
  else:
    print("Login credentials do not match")
  

def train(network, epoch, train_loader, it, optimizer, lr_1000, train_loss_1000, lr_scheduler):
  logging_interval = 2 #After every 2 batches

  network.train()
  train_loss = 0
  for batch_idx, (data, target) in enumerate(train_loader):
    it.append(1)
    optimizer.zero_grad() #
    output = network(data)
    loss = F.nll_loss(output, target) #
    train_loss += loss.item()
    loss.backward()
    optimizer.step()

    lr_1000.append(optimizer.param_groups[0]["lr"])
    train_loss_1000.append(loss.item())

    lr_scheduler.step()

  return network, it, optimizer, lr_1000, train_loss_1000, lr_scheduler

def lr_range_finder(network, train_loader, name):

  #DEFINE OPTIMIZER

  start_lr = 1e-8
  momentum = 0.5
  optimizer = optim.SGD(network.parameters(), lr=start_lr, momentum=momentum)
  lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=1.017)

  #LR RANGE FINDER

  lr_1000 = []
  train_loss_1000 = []
  it = []

  print("Starting LR finder...")
  n_epochs = 80
  for epoch in range(1, n_epochs+1):
    network, it, optimizer, lr_1000, train_loss_1000, lr_scheduler = train(network, epoch, train_loader, it, optimizer, lr_1000, train_loss_1000, lr_scheduler)
    if len(it)>1000:
      break

  metrics = {'lr_1000':lr_1000, 'train_loss_1000':train_loss_1000, 'name': name, 'task':'initLR', 'username': os.environ['username'], 'key': os.environ['key']}
  
  send_data_to_db(metrics)


