# EnvAttributes

### Loads environment into class attributes

## Install:
```bash
pip install env_attributes
```

## Example:

### Environment:
```dotenv
HOST=localhost
PORT=5050
```

### Usage:

#### Variant 1:

```python
from env_attributes import Environment

path_to_env = 'example/.env'
env = Environment(env_path=path_to_env)

print(env.host, env.port)
```
output:
```
localhost 5050
```

#### Variant 2:
Correct if the .env file is in the root directory

```python
from env_attributes import env

print(env.host, env.port)
```
output:
```
localhost 5050
```

### Additional usage:
```
print(env.get('host'), env['port'])
```

#### Register is not important:
```
print(env.get('HoSt'), env['PORT'])
```

#### You can work with the env object as with a dict:
```
for key in env:
    value = env.get(key)
    print(key, value)
```
output:
```
host localhost
port 5050
```

#### You can output all environment variables:
```
print(env)
```
output:
```json
{"host": "localhost", "port": "5050"}
```

#### You can also get all keys or values from env:
```
print(env.keys())
print(env.values())
```
output:
```
['host', 'port']
['localhost', '5050']
```

#### You can get length of env:
```
print(len(env))
```
output:
```
2
```