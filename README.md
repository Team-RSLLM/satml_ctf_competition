<h1 align="center">
  <br>
  Team RSLLM SaTML CTF Competition
  <br>
</h1>

<h4 align="center">Submission evaluation and evaluation scripts for the <a href="https://ctf.spylab.ai/" target="_blank">Large Language Model Capture-the-Flag (LLM CTF) Competition @ SaTML 2024</a> of team RSLLM.</h4>

<p align="center">
  <a href="#usage">Usage</a> •
  <a href="#docs">Docs</a> •
  <a href="#credits">Credits</a>
</p>

---

## Usage
Set your API key

```bash
export API_KEY="your_api_key"
```

### Defense Testing Script
Script to automate the defense testing process.
Goes through all the attacks and evalutes them for a given defense.

```bash
python scripts/testing_defense.py
```

### Competition Attack Script
Script to automate the attack competition.
Starts an attack and allows for interactive prompting in the competition.

```bash
python scripts/competition_attack.py
```

## Docs
- ```attacks/sample_attacks.yaml```: contains a list of sample attacks
- ```defenses/gpt.json```: GPT defense (prompt and filters)
- ```defenses/llama.json```: LLAMA defense (prompt and filters)

## Credits
> Robin Schmid &nbsp;&middot;&nbsp;
> GitHub [@RobinSchmid7](https://github.com/RobinSchmid7) &nbsp;&middot;&nbsp;
> Email [schmidrobin@outlook.ch](mailto:schmidrobin@outlook.ch)

> Takahiro Miki &nbsp;&middot;&nbsp;
> GitHub [@mktk1117](https://github.com/mktk1117) &nbsp;&middot;&nbsp;
> Email [takahiro.miki1992@gmail.com](mailto:takahiro.miki1992@gmail.com)

> Victor Klemm &nbsp;&middot;&nbsp;
> GitHub [@vklemm](https://github.com/vklemm) &nbsp;&middot;&nbsp;
> Email [vklemm@ethz.ch](mailto:vklemm@ethz.ch)

> Chenhao Li &nbsp;&middot;&nbsp;
> GitHub [@breadli428](https://github.com/breadli428) &nbsp;&middot;&nbsp;
> Email [chenhli@ethz.ch](mailto:chenhli@ethz.ch)

> Stefan Kraft &nbsp;&middot;&nbsp;
> GitHub [@stekra](https://github.com/stekra) &nbsp;&middot;&nbsp;
> Email [st3kra@gmail.com](mailto:st3kra@gmail.com)

