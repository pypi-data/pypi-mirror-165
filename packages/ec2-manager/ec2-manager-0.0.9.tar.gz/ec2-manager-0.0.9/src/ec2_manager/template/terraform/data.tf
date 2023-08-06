# ----------------------------------------------------------------------
# AMI with docker installed
# ----------------------------------------------------------------------
data "aws_ami" "amazon_linux" {
  owners = ["amazon"]
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-*-arm64-gp2"]
  }
}

data "aws_vpcs" "selected" {
  filter {
    name   = "tag:Name"
    values = [var.vpc_name]
  }
}

data "aws_subnets" "selected" {
}

data "aws_subnet" "all" {
  for_each = toset(data.aws_subnets.selected.ids)
  id       = each.value
}

data "aws_subnet" "selected" {
  vpc_id = data.aws_vpcs.selected.ids[0]
  cidr_block = local.subnet_cidr_range == "" ? data.aws_subnet.all[data.aws_subnets.selected.ids[0]].cidr_block : local.subnet_cidr_range
}