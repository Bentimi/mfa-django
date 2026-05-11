from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from datetime import datetime

# Brand Colors - Modern Security App Palette
PRIMARY = "#4F46E5"  # Indigo 600
PRIMARY_DARK = "#4338CA"  # Indigo 700
PRIMARY_LIGHT = "#818CF8"  # Indigo 400
SUCCESS = "#10B981"  # Emerald 500
WARNING = "#F59E0B"  # Amber 500
DANGER = "#EF4444"  # Red 500
DARK = "#1E293B"  # Slate 800
GRAY = "#64748B"  # Slate 500
LIGHT_GRAY = "#F1F5F9"  # Slate 100
WHITE = "#FFFFFF"


def _email_base(content: str, accent_color: str = PRIMARY) -> str:
    """Base email template with branded design."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MFA App</title>
</head>
<body style="margin: 0; padding: 0; background-color: {LIGHT_GRAY}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
        <tr>
            <td style="padding: 40px 20px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center" style="max-width: 600px; margin: 0 auto; background-color: {WHITE}; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                    <!-- Header with Logo Area -->
                    <tr>
                        <td style="background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%); padding: 32px 40px; text-align: center;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                <tr>
                                    <td style="text-align: center;">
                                        <span style="color: {WHITE}; font-size: 32px; font-weight: 800; letter-spacing: 2px;">MFA</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Accent Bar -->
                    <tr>
                        <td style="height: 4px; background-color: {accent_color};"></td>
                    </tr>
                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 40px;">
                            {content}
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: {LIGHT_GRAY}; padding: 24px 40px; text-align: center; border-top: 1px solid #E2E8F0;">
                            <p style="margin: 0; color: {GRAY}; font-size: 12px; line-height: 1.5;">
                                This is an automated message from MFA App.<br>
                                Please do not reply to this email.
                            </p>
                            <p style="margin: 16px 0 0 0; color: #94A3B8; font-size: 11px;">
                                © {datetime.now().year} MFA App. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def send_welcome_email(user):
    """Send professionally designed welcome email after successful registration."""
    subject = "Welcome to MFA App! 🎉"
    
    content = f"""
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin-bottom: 32px; text-align: center;">
        <tr>
            <td style="text-align: center;">
                <div style="width: 64px; height: 64px; background: linear-gradient(135deg, {SUCCESS} 0%, #059669 100%); border-radius: 50%; margin: 0 auto 20px; text-align: center; line-height: 64px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                    <span style="color: {WHITE}; font-size: 32px; display: inline-block; vertical-align: middle; line-height: normal;">✓</span>
                </div>
                <h1 style="color: {DARK}; font-size: 28px; font-weight: 700; margin: 0 0 12px 0; letter-spacing: -0.5px;">Welcome aboard!</h1>
                <p style="color: {GRAY}; font-size: 16px; margin: 0;">Your account has been successfully created</p>
            </td>
        </tr>
    </table>
    
    <p style="color: {DARK}; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0;">
        Hi <strong style="color: {PRIMARY};">{user.first_name or 'there'}</strong>,
    </p>
    
    <p style="color: #334155; font-size: 15px; line-height: 1.7; margin: 0 0 20px 0;">
        Thank you for joining <strong>MFA App</strong>. Your account is now ready to use. You can now log in using your email and password with enhanced security through our multi-factor authentication system.
    </p>
    
    <div style="background-color: {LIGHT_GRAY}; border-left: 4px solid {PRIMARY}; padding: 20px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <p style="margin: 0 0 8px 0; color: {DARK}; font-weight: 600; font-size: 14px;">What's next?</p>
        <p style="margin: 0; color: {GRAY}; font-size: 14px; line-height: 1.6;">Log in to your account and explore the secure features we've built for you.</p>
    </div>
    
    <p style="color: {GRAY}; font-size: 13px; line-height: 1.5; margin: 24px 0 0 0; padding-top: 24px; border-top: 1px solid #E2E8F0;">
        If you didn't create this account, please <a href="#" style="color: {PRIMARY}; text-decoration: none; font-weight: 500;">contact our support team</a> immediately.
    </p>
    """
    
    html_message = _email_base(content, accent_color=SUCCESS)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False


def send_otp_email(user, otp):
    """Send professionally designed OTP email for login verification."""
    subject = "Your Verification Code 🔐"
    
    content = f"""
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin-bottom: 32px; text-align: center;">
        <tr>
            <td style="text-align: center;">
                <div style="width: 64px; height: 64px; background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%); border-radius: 50%; margin: 0 auto 20px; text-align: center; line-height: 64px; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);">
                    <span style="color: {WHITE}; font-size: 28px; display: inline-block; vertical-align: middle; line-height: normal;">🔐</span>
                </div>
                <h1 style="color: {DARK}; font-size: 26px; font-weight: 700; margin: 0 0 12px 0; letter-spacing: -0.5px;">Verify Your Login</h1>
                <p style="color: {GRAY}; font-size: 15px; margin: 0;">Use the code below to complete your sign-in</p>
            </td>
        </tr>
    </table>
    
    <p style="color: {DARK}; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0;">
        Hi <strong style="color: {PRIMARY};">{user.first_name or 'there'}</strong>,
    </p>
    
    <p style="color: #334155; font-size: 15px; line-height: 1.7; margin: 0 0 24px 0;">
        We received a login request for your MFA App account. Enter this verification code to continue:
    </p>
    
    <div style="background: linear-gradient(135deg, {LIGHT_GRAY} 0%, #E2E8F0 100%); border: 2px dashed {PRIMARY_LIGHT}; border-radius: 12px; padding: 32px; text-align: center; margin: 24px 0;">
        <p style="margin: 0 0 8px 0; color: {GRAY}; font-size: 13px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase;">Verification Code</p>
        <div style="font-size: 42px; font-weight: 800; letter-spacing: 12px; color: {PRIMARY}; font-family: 'Courier New', monospace; text-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);">
            {otp}
        </div>
    </div>
    
    <div style="background-color: #FEF3C7; border: 1px solid #FCD34D; border-radius: 8px; padding: 16px 20px; margin: 20px 0;">
        <p style="margin: 0; color: #92400E; font-size: 14px; line-height: 1.5;">
            <strong>⏱ Expires in 5 minutes</strong> — For security, this code will expire shortly.
        </p>
    </div>
    
    <div style="background-color: #FEE2E2; border-left: 4px solid {DANGER}; padding: 16px 20px; margin: 20px 0; border-radius: 0 8px 8px 0;">
        <p style="margin: 0; color: #991B1B; font-size: 13px; line-height: 1.5;">
            <strong>Didn't request this?</strong> If you didn't try to log in, someone may be trying to access your account. Please secure your account immediately.
        </p>
    </div>
    
    <p style="color: {GRAY}; font-size: 13px; line-height: 1.5; margin: 24px 0 0 0; padding-top: 24px; border-top: 1px solid #E2E8F0; text-align: center;">
        Never share this code with anyone, including MFA App support.
    </p>
    """
    
    html_message = _email_base(content, accent_color=SUCCESS)
    
    plain_message = f"""
Hi {user.first_name or 'there'},

Your MFA App verification code is: {otp}

This code will expire in 5 minutes.

If you didn't request this login, please secure your account immediately.

Never share this code with anyone.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send OTP email to {user.email}: {str(e)}")
        return False


def send_login_notification(user, ip_address=None, device_info=None):
    """Send professionally designed login notification email."""
    subject = "New Login to Your Account 🔔"
    
    from django.utils import timezone
    login_time = timezone.now().strftime("%B %d, %Y at %I:%M %p UTC")
    
    ip_display = ip_address if ip_address else "Unknown"
    device_display = device_info if device_info else "Unknown device"
    
    content = f"""
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin-bottom: 32px; text-align: center;">
        <tr>
            <td style="text-align: center;">
                <div style="width: 64px; height: 64px; background: linear-gradient(135deg, {WARNING} 0%, #D97706 100%); border-radius: 50%; margin: 0 auto 20px; text-align: center; line-height: 64px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
                    <span style="color: {WHITE}; font-size: 28px; display: inline-block; vertical-align: middle; line-height: normal;">🔔</span>
                </div>
                <h1 style="color: {DARK}; font-size: 26px; font-weight: 700; margin: 0 0 12px 0; letter-spacing: -0.5px;">New Login Detected</h1>
                <p style="color: {GRAY}; font-size: 15px; margin: 0;">We noticed a new sign-in to your account</p>
            </td>
        </tr>
    </table>
    
    <p style="color: {DARK}; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0;">
        Hi <strong style="color: {PRIMARY};">{user.first_name or 'there'}</strong>,
    </p>
    
    <p style="color: #334155; font-size: 15px; line-height: 1.7; margin: 0 0 24px 0;">
        A new device just signed in to your MFA App account on:
    </p>
    
    <div style="background-color: {LIGHT_GRAY}; border-radius: 12px; padding: 24px; margin: 24px 0; text-align: center;">
        <p style="color: {GRAY}; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0;">Time</p>
        <p style="margin: 0; color: {DARK}; font-size: 16px; font-weight: 600;">{login_time}</p>
    </div>
    
    <div style="text-align: center; margin: 32px 0;">
        <p style="color: #059669; font-size: 15px; font-weight: 500; margin: 0 0 8px 0;">✓ Was this you?</p>
        <p style="color: {GRAY}; font-size: 14px; margin: 0;">If yes, you can safely ignore this email.</p>
    </div>
    
    <div style="background-color: #FEE2E2; border-left: 4px solid {DANGER}; padding: 20px 24px; margin: 24px 0; border-radius: 0 8px 8px 0;">
        <p style="margin: 0 0 12px 0; color: #991B1B; font-size: 15px; font-weight: 600;">⚠️ Didn't sign in?</p>
        <p style="margin: 0; color: #7F1D1D; font-size: 14px; line-height: 1.6;">
            Someone may have accessed your account. Please change your password immediately or contact our support team.
        </p>
    </div>
    """
    
    html_message = _email_base(content, accent_color=WARNING)
    
    plain_message = f"""
Hi {user.first_name or 'there'},

New login detected on your MFA App account:

Time: {login_time}

Was this you? If yes, you can safely ignore this email.

If you didn't sign in, someone may have accessed your account. Please change your password immediately or contact our support team.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send login notification to {user.email}: {str(e)}")
        return False
