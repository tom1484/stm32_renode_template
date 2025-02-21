# STM32 Renode Template

## Port the renode debugging to a new project

```bash
# Example
python3 create.py --project-path ../renode_test/ \
    --cpu stm32f429 \
    --board STM32F429ZITx \
    --remote-host "churong.cc" \
    --remote-user tomchen \
    --gdb-port 3333
```
