<p align="center">
<img src="https://github.com/jina-ai/finetuner/blob/main/docs/_static/finetuner-logo-ani.svg?raw=true" alt="Finetuner logo: Finetuner allows one to finetune any deep Neural Network for better embedding on search tasks. It accompanies Jina to deliver the last mile of performance-tuning for neural search applications." width="150px">
</p>


<p align="center">
<b>Finetuning any deep neural network for better embedding on neural search tasks</b>
</p>

<p align=center>
<a href="https://pypi.org/project/finetuner/"><img src="https://img.shields.io/badge/Python-3.8%2B-blue alt="Python 3.8" title="Finetuner supports Python 3.9 and above"></a>
<a href="https://slack.jina.ai"><img src="https://img.shields.io/badge/Slack-2.2k%2B-blueviolet?logo=slack&amp;logoColor=white"></a>
</p>

<!-- start elevator-pitch -->

Finetuner allows one to tune the weights of any deep neural network for better embeddings on search tasks. It
accompanies [Jina](https://github.com/jina-ai/jina) to deliver the last mile of performance for domain-specific neural search
applications.

🎛 **Designed for finetuning**: a deep learning tool for leveling up your pretrained models in domain-specific neural search applications.

🔱 **Powerful yet intuitive**: Finetuner unlocks rich features such as
siamese/triplet network, metric learning, self-supervised pretraining, layer pruning, weights freezing, dimensionality reduction.

🧈 **DocArray integration**: buttery smooth integration with DocArray, reducing the cost of context-switch between experiment
and production.

<!-- end elevator-pitch -->

## Install

Requires Python 3.8 and [PyTorch](https://pytorch.org/)(>=1.9) installed on Linux/MacOS.

To install the `finetuner-core` repo:
```bash
python setup.py --target=finetuner install
```

To only install the shared components between `finetuner-core` and `finetuner-client`:

```bash
python setup.py --target=commons install  # include tailor, process, collate
python setup.py --target=stubs install  # include all model stubs and callback stubs and config
```

<!-- start support-pitch -->
## Support

- Use [Discussions](https://github.com/jina-ai/finetuner/discussions) to talk about your use cases, questions, and
  support queries.
- Join our [Slack community](https://slack.jina.ai) and chat with other Jina community members about ideas.
- Join our [Engineering All Hands](https://youtube.com/playlist?list=PL3UBBWOUVhFYRUa_gpYYKBqEAkO4sxmne) meet-up to discuss your use case and learn Jina's new features.
    - **When?** The second Tuesday of every month
    - **Where?**
      Zoom ([see our public events calendar](https://calendar.google.com/calendar/embed?src=c_1t5ogfp2d45v8fit981j08mcm4%40group.calendar.google.com&ctz=Europe%2FBerlin)/[.ical](https://calendar.google.com/calendar/ical/c_1t5ogfp2d45v8fit981j08mcm4%40group.calendar.google.com/public/basic.ics))
      and [live stream on YouTube](https://youtube.com/c/jina-ai)
- Subscribe to the latest video tutorials on our [YouTube channel](https://youtube.com/c/jina-ai)

## Join Us

Finetuner is backed by [Jina AI](https://jina.ai) and licensed under [Apache-2.0](./LICENSE). [We are actively hiring](https://jobs.jina.ai) AI engineers, solution engineers to build the next neural search ecosystem in opensource.

<!-- end support-pitch -->