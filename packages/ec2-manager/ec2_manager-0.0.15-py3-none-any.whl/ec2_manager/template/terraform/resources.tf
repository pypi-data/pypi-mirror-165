
module "ec2_instance" {
  for_each = local.instances
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "3.5.0"

  name = each.key
  cpu_credits = "standard"
  create_spot_instance = true
  spot_type = "persistent"
  ami = data.aws_ami.amazon_linux.id
  iam_instance_profile = aws_iam_instance_profile.ec2_tag_profile.name
  instance_type = each.value.instance_type
  monitoring = false
  vpc_security_group_ids = [aws_security_group.instance_security_group[each.key].id]
  subnet_id = data.aws_subnet.selected.id
  user_data_base64 = base64encode(
     templatefile(local.user_data_file,
     {
       envs = {
         AWS_REGION=var.aws_region
         EXPOSE_DOCKER_DAEMON=var.expose_docker_daemons
       }
     })
  )
  tags = {
    Name = each.key
    Type = var.type
  }
  enable_volume_tags = false
  root_block_device = [
    {
      encrypted   = false
      volume_type = "gp3"
      volume_size = each.value.volume_size
      tags = {
        Name = each.key
        Type = var.type
      }
    }
  ]
}