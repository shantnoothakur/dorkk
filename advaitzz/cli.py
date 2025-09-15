#!/usr/bin/env python3
})
return results




@click.command()
@click.argument('domains', required=False)
@click.option('--input', '-i', 'input_file', type=click.Path(exists=True), help='File with domains (one per line)')
@click.option('--categories', '-c', default='login,sensitive,docs,index,subdomains', help='Comma separated categories')
@click.option('--output', '-o', default=None, help='Output filename')
@click.option('--format', 'outfmt', default='txt', type=click.Choice(['txt', 'csv']), help='Output format')
@click.option('--all', 'allcats', is_flag=True, help='Generate all categories')
@click.option('--quiet', is_flag=True, help='Quiet mode (minimal output)')
def main(domains, input_file, categories, output, outfmt, allcats, quiet):
"""ADVAITZZ - generate Google dorks for one or many domains.


Example:
advaitzz example.com
advaitzz --input domains.txt --categories login,docs --output dorks.txt
"""
if not domains and not input_file:
# interactive fallback
domain = click.prompt('Enter target domain')
domains = domain


domain_list = []
if input_file:
p = Path(input_file)
domain_list = [l.strip() for l in p.read_text().splitlines() if l.strip()]
elif isinstance(domains, str):
domain_list = [domains]
else:
domain_list = list(domains)


selected = [c.strip() for c in categories.split(',') if c.strip()]
if allcats:
selected = list(TEMPLATES.keys())


all_results = []
for d in domain_list:
r = generate_for_domain(d, selected)
all_results.extend(r)


if not quiet:
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Domain")
table.add_column("Category")
table.add_column("Dork")
for row in all_results:
table.add_row(row['domain'], row['category'], row['dork'])
console.print(table)


if output:
if outfmt == 'txt':
with open(output, 'w') as fh:
for row in all_results:
fh.write(row['dork'] + "\n")
elif outfmt == 'csv':
df = pd.DataFrame(all_results)
df.to_csv(output, index=False)
if not quiet:
console.print(f"Saved {len(all_results)} dorks to {output}")


# For scripting usage, also print to stdout if quiet
if quiet and not output:
for row in all_results:
print(row['dork'])




if __name__ == '__main__':
main()
