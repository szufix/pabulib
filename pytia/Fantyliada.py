

from pabutools.election import parse_pabulib

file_name = 'poland_warszawa_2023_wawer'
path = f'pabulib/{file_name}.pb'
instance, profile = parse_pabulib(path)
