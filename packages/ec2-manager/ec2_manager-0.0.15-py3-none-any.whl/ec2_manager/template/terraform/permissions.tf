resource "aws_security_group" "instance_security_group" {
  for_each = local.instances
  name = "${each.key}-security-group"
  description = "Defines ingress and egress rules for the ${each.key} instance"

  vpc_id = data.aws_vpcs.selected.ids[0]

  # allows a connection to the freqtrade ui
  dynamic "ingress" {
    for_each = each.value.ports
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = [local.to_cidr_range]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}
// Create a generic SSM policy
resource "aws_iam_policy" "ec2_tag_policy" {
  name = "${var.type}-ec2-policy"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            Effect: "Allow",
            Action: [
                "ec2:CreateTags",
                "ec2:DescribeInstances",
                "ec2:DescribeSpotInstanceRequests"
            ],
            Resource: "*"
        }
    ]
  })
}

// Create a generic role with a ec2 trust policy
resource "aws_iam_role" "ec2_role" {
  name = "${var.type}-ec2-role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        Effect: "Allow",
        Principal: {
          Service: "ec2.amazonaws.com"
        },
        Action: "sts:AssumeRole"
      }
    ]
  })
}

// Attach the role to the policy file
resource "aws_iam_policy_attachment" "ec2_tag_policy_attachment" {
  name = "${var.type}-ec2-tag"
  roles = [aws_iam_role.ec2_role.name]
  policy_arn = aws_iam_policy.ec2_tag_policy.arn
}

resource "aws_iam_policy_attachment" "ec2_ssm_policy_attachment" {
  name = "${var.type}-ec2-ssm"
  roles = [aws_iam_role.ec2_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
}

// Create an instance profile
resource "aws_iam_instance_profile" "ec2_tag_profile" {
  name = "${var.type}-ec2-instance-profile"
  role = aws_iam_role.ec2_role.name
}