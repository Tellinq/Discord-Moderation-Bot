import disnake
from disnake.ext import plugins


plugin = plugins.Plugin()


@plugin.slash_command()
async def info(inter: disnake.CmdInter):
    pass


@info.sub_command()
async def user(inter: disnake.CmdInter, target: disnake.User):
    """
    Get details about a user/member

    Parameters
    ----------
    target: The user/member to get details of
    """
    
    # format the username based on if they are still using discrims or not
    username = f"@{target}" if target.discriminator == "0" else target
    
    embed = disnake.Embed(title=username)
    embed.set_footer(text=f"ID: {target.id}")
    embed.set_thumbnail(target.display_avatar)
    
    embed.add_field(
        "Created",
        disnake.utils.format_dt(target.created_at, "R"),
        inline=False
    )
    
    if isinstance(target, disnake.Member):
        embed.add_field(
            "Joined",
            disnake.utils.format_dt(target.joined_at, "R"),
            inline=False
        )
        
        roles = target.roles[1:] # exclude @everyone
        
        if roles:
            embed.add_field(
                f"Roles [{len(roles)}]",
                ", ".join(role.mention for role in roles),
                inline=False
            )
        
    await inter.send(embed=embed)
    
    
@info.sub_command()
async def server(inter: disnake.CmdInter):
    """Get details about the server"""
    
    embed = disnake.Embed(
        title=inter.guild.name,
        description=inter.guild.description
    )
    
    embed.set_thumbnail(inter.guild.icon)
    
    embed.add_field(
        "Owner",
        inter.guild.owner.mention,
        inline=False
    )
    
    embed.add_field(
        "Created",
        disnake.utils.format_dt(inter.guild.created_at, "R"),
        inline=False
    )
    
    embed.add_field(
        "Members",
        inter.guild.member_count,
        inline=False
    )
    
    await inter.send(embed=embed)
    


setup, teardown = plugin.create_extension_handlers()